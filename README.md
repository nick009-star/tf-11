# Loja refatorada

## 1. Normalizacao
Antes, cada compra repetia os dados da Ana, então uma mudança de endereço poderia deixar os pedidos inconsistentes.
Agora os pedidos 1 e 3 apontam para o mesmo objeto Cliente, mantendo uma única versão desses dados.

## 2. Tipos primitivos
Cpf virou uma classe para impedir que um identificador malformado circule pelo sistema como se fosse válido.
Dinheiro armazena centavos inteiros, evitando erros de representação e de soma comuns com valores `float`.

## 3. Diga, nao pergunte
O pagamento é solicitado ao pedido, que verifica se continua aberto e se possui itens antes de mudar seu estado.
Assim, a regra e a transição ficam juntas, em vez de espalhadas entre quem consulta e altera o status.

## 4. Fail first
A validação antiga encadeava decisões dentro de `valida`; agora os tipos rejeitam dados inválidos ao serem criados e a loja apresenta o motivo.
Retornos antecipados deixam os casos recusados explícitos, e os tipos de cliente aplicam descontos sem ramificações por código.

## 5. Modularizacao
- `Cpf`: valida o comprimento do CPF.
- `Email`: valida presença e formato básico do email.
- `Cep`: valida o comprimento do CEP.
- `Dinheiro`: representa centavos e realiza operações monetárias.
- `Status`: descreve e altera o estado de um pedido.
- `Pessoa`: reúne nome e identificadores pessoais.
- `Endereco`: reúne rua, cidade e CEP.
- `Cliente`: combina pessoa, endereço e política de desconto.
- `TipoNormal`: aplica desconto de zero por cento.
- `TipoVip`: aplica desconto de dez por cento.
- `TipoFuncionario`: aplica desconto de vinte por cento.
- `Produto`: guarda o nome e o preço de um produto.
- `ItemDoPedido`: associa um produto à quantidade comprada.
- `ItensDoPedido`: administra itens e calcula seu total.
- `Pedido`: aplica as regras de pagamento e apresenta o pedido.
- `Pedidos`: organiza pedidos por número e calcula os totais da loja.

## 6. Divida tecnica
Não identifiquei regra pendente nem atalho intencional nesta versão.
A Lei de Demeter foi a mais trabalhosa: exigiu dar às classes operações de apresentação e cálculo, em vez de navegar pelos dados umas das outras.
