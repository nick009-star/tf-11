# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []


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


class Cliente:
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.nome = nome
        self.email = Email(email)
        self.cpf = Cpf(cpf)
        self.rua = rua
        self.cidade = cidade
        self.cep = Cep(cep)
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


class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []
        self.status = Status("A")

    def get_status(self):
        return self.status

    def set_status(self, valor):
        self.status = Status(valor)


def novo_pedido(numero, cliente):
    pedido = Pedido(numero, cliente)
    pedidos.append(pedido)
    return pedido


def recusar_pedido(numero, email, cpf, cep):
    try:
        Email(email)
        Cpf(cpf)
        Cep(cep)
    except ValueError as erro:
        print("pedido", numero, "recusado:", erro)


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def calcular_total(pedido):
    total = Dinheiro(0)
    for item in pedido.itens:
        total = total.somar(item.calcular_total())
    return total


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
        if len(pedido.itens) > 0:
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


def relatorio():
    for pedido in pedidos:
        print("Pedido", pedido.numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
        print("  status:", descrever_status(pedido.get_status()))
        for item in pedido.itens:
            print("  ", item.quantidade, "x", item.produto.nome, "=", item.calcular_total())
        if len(pedido.itens) > 0:
            print("  total:", calcular_total(pedido), "| desconto:", calcular_desconto(pedido.cliente.tipo, calcular_total(pedido)), "| a pagar:", calcular_valor_a_pagar(pedido))


def arrecadado():
    total_arrecadado = Dinheiro(0)
    for pedido in pedidos:
        if pedido.get_status().esta_pago():
            total_arrecadado = total_arrecadado.somar(calcular_valor_a_pagar(pedido))
    return total_arrecadado


def quantidade_de_pedidos_abertos():
    quantidade = 0
    for pedido in pedidos:
        if pedido.get_status().esta_aberto():
            quantidade = quantidade + 1
    return quantidade


# --- o roteiro da loja ---------------------------------------------------------
cliente_ana = Cliente("Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
pedido_da_ana = novo_pedido(1, cliente_ana)
adicionar_item(pedido_da_ana, Produto("Caderno", Dinheiro(1550)), 2)
adicionar_item(pedido_da_ana, Produto("Caneta", Dinheiro(250)), 5)

recusar_pedido(2, "bruno@mail.com", "123", "18110000")

pedido_da_ana_terceiro = novo_pedido(3, cliente_ana)
adicionar_item(pedido_da_ana_terceiro, Produto("Livro", Dinheiro(8950)), 1)

recusar_pedido(4, "carla.mail.com", "98765432100", "18020000")

cliente_diego = Cliente("Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")
pedido_do_diego = novo_pedido(5, cliente_diego)

cliente_eva = Cliente("Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
pedido_da_eva = novo_pedido(6, cliente_eva)
fone = Produto("Fone", Dinheiro(6000))
adicionar_item(pedido_da_eva, fone, 1)

recusar_pedido(7, "fabio@mail.com", "99988877766", "123")

cliente_gil = Cliente("Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")
pedido_do_gil = novo_pedido(8, cliente_gil)
adicionar_item(pedido_do_gil, fone, 2)

print("pagar 1:", pagar(pedido_da_ana))
print("pagar 3:", pagar(pedido_da_ana_terceiro))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(pedido_da_ana))

relatorio()
print("arrecadado:", arrecadado())
print("abertos:", quantidade_de_pedidos_abertos())
