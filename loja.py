# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

class Cpf:
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self.valor = valor


class Email:
    def __init__(self, valor):
        if len(valor) == 0:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self.valor = valor


class Cep:
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self.valor = valor


class Dinheiro:
    def __init__(self, centavos):
        self.centavos = centavos

    def somar(self, outro):
        return Dinheiro(self.centavos + outro.centavos)

    def subtrair(self, outro):
        return Dinheiro(self.centavos - outro.centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self.centavos * quantidade)

    def percentual(self, percentual):
        return Dinheiro((self.centavos * percentual + 50) // 100)

    def __str__(self):
        return "R$ %.2f" % (self.centavos / 100)


class Status:
    def __init__(self, codigo):
        self.codigo = codigo

    def descricao(self):
        return {"A": "aberto", "P": "pago", "C": "cancelado"}[self.codigo]

    def esta_aberto(self):
        return self.codigo == "A"

    def esta_pago(self):
        return self.codigo == "P"


class Pessoa:
    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.email = Email(email)
        self.cpf = Cpf(cpf)
 

class Endereco:
    def __init__(self, rua, cidade, cep):
        self.rua = rua
        self.cidade = cidade
        self.cep = Cep(cep)


class Cliente:
    def __init__(self, pessoa, endereco, tipo):
        self.pessoa = pessoa
        self.endereco = endereco
        self.tipo = tipo


class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco

    def calcular_valor(self, quantidade):
        return self.preco.multiplicar(quantidade)


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def calcular_total(self):
        return self.produto.calcular_valor(self.quantidade)


class ItensDoPedido:
    def __init__(self):
        self.itens = []

    def adicionar(self, item):
        self.itens.append(item)

    def esta_vazia(self):
        return len(self.itens) == 0

    def calcular_total(self):
        total = Dinheiro(0)
        for item in self.itens:
            total = total.somar(item.calcular_total())
        return total

    def imprimir(self):
        for item in self.itens:
            print("  ", item.quantidade, "x", item.produto.nome, "=", item.calcular_total())


class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = ItensDoPedido()
        self.status = Status("A")

    def get_status(self):
        return self.status

    def set_status(self, valor):
        self.status = Status(valor)


def recusar_pedido(numero, email, cpf, cep):
    try:
        Email(email)
        Cpf(cpf)
        Cep(cep)
    except ValueError as erro:
        print("pedido", numero, "recusado:", erro)


def calcular_total(pedido):
    return pedido.itens.calcular_total()


def calcular_desconto(tipo, total):
    if tipo == "V":
        desconto = total.percentual(10)
    elif tipo == "F":
        desconto = total.percentual(20)
    else:
        return Dinheiro(0)
    return desconto


def calcular_valor_a_pagar(pedido):
    return calcular_total(pedido).subtrair(calcular_desconto(pedido.cliente.tipo, calcular_total(pedido)))


def pagar(pedido):
    if pedido.get_status().esta_aberto():
        if not pedido.itens.esta_vazia():
            pedido.set_status("P")
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status().esta_aberto():
        pedido.set_status("C")
        return True
    else:
        return False


def descrever_status(status):
    return status.descricao()


class Pedidos:
    def __init__(self):
        self.pedidos = {}

    def novo_pedido(self, numero, cliente):
        pedido = Pedido(cliente)
        self.pedidos[numero] = pedido
        return pedido

    def adicionar_item(self, numero, produto, quantidade):
        self.pedidos[numero].itens.adicionar(ItemDoPedido(produto, quantidade))

    def pagar(self, numero):
        return pagar(self.pedidos[numero])

    def cancelar(self, numero):
        return cancelar(self.pedidos[numero])

    def relatorio(self):
        for numero, pedido in self.pedidos.items():
            print("Pedido", numero, "-", pedido.cliente.pessoa.nome, "-", pedido.cliente.endereco.cidade)
            print("  status:", descrever_status(pedido.get_status()))
            pedido.itens.imprimir()
            if not pedido.itens.esta_vazia():
                print("  total:", calcular_total(pedido), "| desconto:", calcular_desconto(pedido.cliente.tipo, calcular_total(pedido)), "| a pagar:", calcular_valor_a_pagar(pedido))

    def arrecadado(self):
        total_arrecadado = Dinheiro(0)
        for pedido in self.pedidos.values():
            if pedido.get_status().esta_pago():
                total_arrecadado = total_arrecadado.somar(calcular_valor_a_pagar(pedido))
        return total_arrecadado

    def quantidade_de_pedidos_abertos(self):
        quantidade = 0
        for pedido in self.pedidos.values():
            if pedido.get_status().esta_aberto():
                quantidade = quantidade + 1
        return quantidade


# --- o roteiro da loja ---------------------------------------------------------
pedidos = Pedidos()
cliente_ana = Cliente(Pessoa("Ana Souza", "12345678901", "ana@mail.com"), Endereco("Rua das Flores, 10", "Sorocaba", "18010000"), "V")
pedido_da_ana = pedidos.novo_pedido(1, cliente_ana)
pedidos.adicionar_item(1, Produto("Caderno", Dinheiro(1550)), 2)
pedidos.adicionar_item(1, Produto("Caneta", Dinheiro(250)), 5)

recusar_pedido(2, "bruno@mail.com", "123", "18110000")

pedido_da_ana_terceiro = pedidos.novo_pedido(3, cliente_ana)
pedidos.adicionar_item(3, Produto("Livro", Dinheiro(8950)), 1)

recusar_pedido(4, "carla.mail.com", "98765432100", "18020000")

cliente_diego = Cliente(Pessoa("Diego Rocha", "11122233344", "diego@mail.com"), Endereco("Rua Nova, 7", "Itu", "13300000"), "N")
pedido_do_diego = pedidos.novo_pedido(5, cliente_diego)

cliente_eva = Cliente(Pessoa("Eva Nunes", "55566677788", "eva@mail.com"), Endereco("Alameda Azul, 1", "Itu", "13300001"), "F")
pedido_da_eva = pedidos.novo_pedido(6, cliente_eva)
fone = Produto("Fone", Dinheiro(6000))
pedidos.adicionar_item(6, fone, 1)

recusar_pedido(7, "fabio@mail.com", "99988877766", "123")

cliente_gil = Cliente(Pessoa("Gil Alves", "44455566677", "gil@mail.com"), Endereco("Rua do Meio, 9", "Sorocaba", "18030000"), "N")
pedido_do_gil = pedidos.novo_pedido(8, cliente_gil)
pedidos.adicionar_item(8, fone, 2)

print("pagar 1:", pedidos.pagar(1))
print("pagar 3:", pedidos.pagar(3))
print("pagar 5:", pedidos.pagar(5))
print("pagar 6:", pedidos.pagar(6))
print("cancelar 5:", pedidos.cancelar(5))
print("cancelar 1:", pedidos.cancelar(1))

pedidos.relatorio()
print("arrecadado:", pedidos.arrecadado())
print("abertos:", pedidos.quantidade_de_pedidos_abertos())
