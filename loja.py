class Cpf:
    # Mantem um CPF que ja passou pela regra de tamanho.
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self._valor = valor


class Email:
    # Mantem um email que ja passou pelas regras basicas.
    def __init__(self, valor):
        if len(valor) == 0:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self._valor = valor


class Cep:
    # Mantem um CEP com oito caracteres.
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self._valor = valor


class Dinheiro:
    # Representa dinheiro em centavos inteiros e concentra suas operacoes.
    def __init__(self, centavos):
        self._centavos = centavos

    def somar(self, outro):
        return Dinheiro(self._centavos + outro._centavos)

    def subtrair(self, outro):
        return Dinheiro(self._centavos - outro._centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self._centavos * quantidade)

    def percentual(self, percentual):
        return Dinheiro((self._centavos * percentual + 50) // 100)

    def __str__(self):
        return "R$ %.2f" % (self._centavos / 100)


class Status:
    # Conhece os estados possiveis e suas transicoes textuais.
    def __init__(self, codigo):
        self._codigo = codigo

    def descricao(self):
        return {"A": "aberto", "P": "pago", "C": "cancelado"}[self._codigo]

    def esta_aberto(self):
        return self._codigo == "A"

    def esta_pago(self):
        return self._codigo == "P"

    def marcar_pago(self):
        self._codigo = "P"

    def marcar_cancelado(self):
        self._codigo = "C"


class Pessoa:
    # Agrupa os dados pessoais e valida os identificadores ao nascer.
    def __init__(self, nome, cpf, email):
        self._nome = nome
        self._email = Email(email)
        self._cpf = Cpf(cpf)

    def imprimir_nome(self):
        print(self._nome, end="")


class Endereco:
    # Guarda o endereco e valida o CEP recebido.
    def __init__(self, rua, cidade, cep):
        self._rua = rua
        self._cidade = cidade
        self._cep = Cep(cep)

    def imprimir_cidade(self):
        print(self._cidade)


class Cliente:
    # Junta pessoa, endereco e a politica de desconto do cliente.
    def __init__(self, pessoa, endereco, tipo):
        self._pessoa = pessoa
        self._endereco = endereco
        self._tipo = tipo

    def imprimir_identificacao(self, numero):
        print("Pedido", numero, "-", end=" ")
        pessoa = self._pessoa
        pessoa.imprimir_nome()
        print(" -", end=" ")
        endereco = self._endereco
        endereco.imprimir_cidade()

    def desconto_sobre(self, total):
        tipo = self._tipo
        return tipo.desconto_sobre(total)


class TipoNormal:
    # Define desconto zero para clientes sem categoria especial.
    def desconto_sobre(self, valor):
        return Dinheiro(0)


class TipoVip:
    # Define o desconto de dez por cento para clientes VIP.
    def desconto_sobre(self, valor):
        return valor.percentual(10)


class TipoFuncionario:
    # Define o desconto de vinte por cento para funcionarios.
    def desconto_sobre(self, valor):
        return valor.percentual(20)


class Produto:
    # Guarda uma unica definicao de produto e calcula valores por quantidade.
    def __init__(self, nome, preco):
        self._nome = nome
        self._preco = preco

    def calcular_valor(self, quantidade):
        preco = self._preco
        return preco.multiplicar(quantidade)

    def imprimir_item(self, quantidade):
        valor = self.calcular_valor(quantidade)
        print("  ", quantidade, "x", self._nome, "=", valor)


class ItemDoPedido:
    # Liga um produto a quantidade comprada no pedido.
    def __init__(self, produto, quantidade):
        self._produto = produto
        self._quantidade = quantidade

    def calcular_total(self):
        produto = self._produto
        quantidade = self._quantidade
        return produto.calcular_valor(quantidade)

    def imprimir(self):
        produto = self._produto
        quantidade = self._quantidade
        produto.imprimir_item(quantidade)


class ItensDoPedido:
    # Controla os itens de um pedido sem expor a lista interna.
    def __init__(self):
        self._itens = []

    def adicionar(self, item):
        itens = self._itens
        itens.append(item)

    def esta_vazia(self):
        return len(self._itens) == 0

    def calcular_total(self):
        total = Dinheiro(0)
        itens = self._itens
        for item in itens:
            valor = item.calcular_total()
            total = total.somar(valor)
        return total

    def imprimir(self):
        itens = self._itens
        for item in itens:
            item.imprimir()


class Pedido:
    # Aplica as regras de pagamento e produz o resumo de um pedido.
    def __init__(self, cliente):
        self._cliente = cliente
        self._itens = ItensDoPedido()
        self._status = Status("A")

    def adicionar_item(self, item):
        itens = self._itens
        itens.adicionar(item)

    def pagar(self):
        status = self._status
        if not status.esta_aberto():
            return False
        itens = self._itens
        if itens.esta_vazia():
            return False
        status.marcar_pago()
        return True

    def cancelar(self):
        status = self._status
        if not status.esta_aberto():
            return False
        status.marcar_cancelado()
        return True

    def esta_pago(self):
        status = self._status
        return status.esta_pago()

    def esta_aberto(self):
        status = self._status
        return status.esta_aberto()

    def calcular_valor_a_pagar(self):
        itens = self._itens
        cliente = self._cliente
        total = itens.calcular_total()
        desconto = cliente.desconto_sobre(total)
        return total.subtrair(desconto)

    def imprimir(self, numero):
        cliente = self._cliente
        status = self._status
        itens = self._itens
        cliente.imprimir_identificacao(numero)
        print("  status:", status.descricao())
        itens.imprimir()
        if not itens.esta_vazia():
            total = itens.calcular_total()
            desconto = cliente.desconto_sobre(total)
            valor_a_pagar = total.subtrair(desconto)
            print("  total:", total, "| desconto:", desconto, "| a pagar:", valor_a_pagar)


class Pedidos:
    # Centraliza os pedidos por numero e agrega seus relatorios e totais.
    def __init__(self):
        self._pedidos = {}

    def novo_pedido(self, numero, cliente):
        pedido = Pedido(cliente)
        self._pedidos[numero] = pedido
        return pedido

    def adicionar_item(self, numero, produto, quantidade):
        item = ItemDoPedido(produto, quantidade)
        pedidos = self._pedidos
        pedido = pedidos[numero]
        pedido.adicionar_item(item)

    def pagar(self, numero):
        pedidos = self._pedidos
        pedido = pedidos[numero]
        return pedido.pagar()

    def cancelar(self, numero):
        pedidos = self._pedidos
        pedido = pedidos[numero]
        return pedido.cancelar()

    def relatorio(self):
        pedidos = self._pedidos
        for numero, pedido in pedidos.items():
            pedido.imprimir(numero)

    def arrecadado(self):
        return self._somar_pedidos_pagos()

    def _somar_pedidos_pagos(self):
        total_arrecadado = Dinheiro(0)
        pedidos = self._pedidos
        for pedido in pedidos.values():
            total_arrecadado = self._somar_se_pago(total_arrecadado, pedido)
        return total_arrecadado

    def quantidade_de_pedidos_abertos(self):
        return self._contar_pedidos_abertos()

    def _contar_pedidos_abertos(self):
        quantidade = 0
        pedidos = self._pedidos
        for pedido in pedidos.values():
            quantidade = quantidade + self._quantidade_se_aberto(pedido)
        return quantidade

    def _somar_se_pago(self, total, pedido):
        if not pedido.esta_pago():
            return total
        valor_a_pagar = pedido.calcular_valor_a_pagar()
        return total.somar(valor_a_pagar)

    def _quantidade_se_aberto(self, pedido):
        if not pedido.esta_aberto():
            return 0
        return 1


def recusar_pedido(numero, email, cpf, cep):
    try:
        Email(email)
        Cpf(cpf)
        Cep(cep)
    except ValueError as erro:
        print("pedido", numero, "recusado:", erro)


# --- o roteiro da loja preserva a sequencia original --------------------------
pedidos = Pedidos()
cliente_ana = Cliente(Pessoa("Ana Souza", "12345678901", "ana@mail.com"), Endereco("Rua das Flores, 10", "Sorocaba", "18010000"), TipoVip())
pedidos.novo_pedido(1, cliente_ana)
pedidos.adicionar_item(1, Produto("Caderno", Dinheiro(1550)), 2)
pedidos.adicionar_item(1, Produto("Caneta", Dinheiro(250)), 5)

recusar_pedido(2, "bruno@mail.com", "123", "18110000")

pedidos.novo_pedido(3, cliente_ana)
pedidos.adicionar_item(3, Produto("Livro", Dinheiro(8950)), 1)

recusar_pedido(4, "carla.mail.com", "98765432100", "18020000")

cliente_diego = Cliente(Pessoa("Diego Rocha", "11122233344", "diego@mail.com"), Endereco("Rua Nova, 7", "Itu", "13300000"), TipoNormal())
pedidos.novo_pedido(5, cliente_diego)

cliente_eva = Cliente(Pessoa("Eva Nunes", "55566677788", "eva@mail.com"), Endereco("Alameda Azul, 1", "Itu", "13300001"), TipoFuncionario())
pedidos.novo_pedido(6, cliente_eva)
fone = Produto("Fone", Dinheiro(6000))
pedidos.adicionar_item(6, fone, 1)

recusar_pedido(7, "fabio@mail.com", "99988877766", "123")

cliente_gil = Cliente(Pessoa("Gil Alves", "44455566677", "gil@mail.com"), Endereco("Rua do Meio, 9", "Sorocaba", "18030000"), TipoNormal())
pedidos.novo_pedido(8, cliente_gil)
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
