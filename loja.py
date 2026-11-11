# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []


class Cliente:
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo


class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade


class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []
        self.status = "A"

    def get_status(self):
        return self.status

    def set_status(self, valor):
        self.status = valor


def validar(email, cpf, cep):
    if len(email) > 0:
        if "@" in email:
            if len(cpf) == 11:
                if len(cep) == 8:
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def novo_pedido(numero, cliente):
    pedido = Pedido(numero, cliente)
    pedidos.append(pedido)
    return pedido


def recusar_pedido(numero, email, cpf, cep):
    resultado = validar(email, cpf, cep)
    if resultado != "ok":
        print("pedido", numero, "recusado:", resultado)


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def calcular_total(pedido):
    total = 0
    for item in pedido.itens:
        total = total + item.quantidade * item.produto.preco
    return total


def calcular_desconto(tipo, total):
    if tipo == "V":
        desconto = total * 0.10
    elif tipo == "F":
        desconto = total * 0.20
    else:
        desconto = 0
    return desconto


def calcular_valor_a_pagar(pedido):
    return calcular_total(pedido) - calcular_desconto(pedido.cliente.tipo, calcular_total(pedido))


def pagar(pedido):
    if pedido.get_status() == "A":
        if len(pedido.itens) > 0:
            pedido.set_status("P")
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status() == "A":
        pedido.set_status("C")
        return True
    else:
        return False


def descrever_status(status):
    if status == "A":
        return "aberto"
    elif status == "P":
        return "pago"
    else:
        return "cancelado"


def relatorio():
    for pedido in pedidos:
        print("Pedido", pedido.numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
        print("  status:", descrever_status(pedido.get_status()))
        for item in pedido.itens:
            print("  ", item.quantidade, "x", item.produto.nome, "= R$ %.2f" % (item.quantidade * item.produto.preco))
        if len(pedido.itens) > 0:
            print("  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f" % (calcular_total(pedido), calcular_desconto(pedido.cliente.tipo, calcular_total(pedido)), calcular_valor_a_pagar(pedido)))


def arrecadado():
    total_arrecadado = 0
    for pedido in pedidos:
        if pedido.get_status() == "P":
            total_arrecadado = total_arrecadado + calcular_valor_a_pagar(pedido)
    return total_arrecadado


def quantidade_de_pedidos_abertos():
    quantidade = 0
    for pedido in pedidos:
        if pedido.get_status() == "A":
            quantidade = quantidade + 1
    return quantidade


# --- o roteiro da loja ---------------------------------------------------------
cliente_ana = Cliente("Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
pedido_da_ana = novo_pedido(1, cliente_ana)
adicionar_item(pedido_da_ana, Produto("Caderno", 15.5), 2)
adicionar_item(pedido_da_ana, Produto("Caneta", 2.5), 5)

recusar_pedido(2, "bruno@mail.com", "123", "18110000")

pedido_da_ana_terceiro = novo_pedido(3, cliente_ana)
adicionar_item(pedido_da_ana_terceiro, Produto("Livro", 89.5), 1)

recusar_pedido(4, "carla.mail.com", "98765432100", "18020000")

cliente_diego = Cliente("Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")
pedido_do_diego = novo_pedido(5, cliente_diego)

cliente_eva = Cliente("Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
pedido_da_eva = novo_pedido(6, cliente_eva)
fone = Produto("Fone", 60.0)
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
print("arrecadado: R$ %.2f" % arrecadado())
print("abertos:", quantidade_de_pedidos_abertos())
