# Caixa Eletrônico — Teste Técnico

Sistema de caixa eletrônico em Python, com interface de console, desenvolvido com foco em Orientação a Objetos e princípios SOLID. Usa apenas a biblioteca padrão da linguagem.

## Requisitos

- Python 3.10 ou superior
- Nenhuma dependência externa

## Como executar

Na pasta raiz do projeto:

```bash
python main.py
```

Para rodar os testes:

```bash
python -m unittest
```

## Contas de teste

| Identificador | Tipo     | Saldo inicial |
|---------------|----------|---------------|
| `1001`        | Cliente  | R$ 2.500,00   |
| `1002`        | Cliente  | R$ 80,00      |
| `admin`       | Operador | —             |

Toda interação começa pelo identificador da conta. Clientes podem consultar o saldo e sacar. O operador pode consultar o estoque, carregar e descarregar cédulas/moedas e ver o log de eventos.

## Estoque inicial

| Denominação     | Quantidade |
|-----------------|------------|
| Cédula R$ 200   | 5          |
| Cédula R$ 100   | 10         |
| Cédula R$ 50    | 10         |
| Cédula R$ 20    | 20         |
| Cédula R$ 10    | 20         |
| Cédula R$ 5     | 20         |
| Cédula R$ 2     | 30         |
| Moeda R$ 1      | 50         |

Novas denominações podem ser incluídas em `ESTOQUE_INICIAL` (`main.py`) ou carregadas pelo menu do operador, sem alterar o código do inventário.

## Estrutura do projeto

```
caixa_eletronico/
├── main.py                  # Interface de console e montagem das dependências
├── caixa/
│   ├── dinheiro.py          # Denominacao, formatação e conversão de valores
│   ├── excecoes.py          # Erros de domínio
│   ├── inventario.py        # Gestão do estoque de cédulas/moedas (Questão 1)
│   ├── estrategias.py       # Contrato e estratégias de composição (Questão 2)
│   ├── sugestoes.py         # Sugestão de valores alternativos (Questão 4)
│   ├── servico_saque.py     # Execução do saque (Questões 2 e 4)
│   ├── notificacao.py       # Notificadores de eventos (Questão 3)
│   ├── contas.py            # Contas de usuário (Questão 5)
│   └── caixa_eletronico.py  # Fachada que integra todas as operações
└── tests/
```

## Estratégias de saque

No momento do saque, o usuário escolhe a estratégia de composição:

1. **Menor quantidade:** entrega o valor com o menor número possível de cédulas.
2. **Preservar cédulas grandes:** usa ao máximo as cédulas de menor valor, poupando as de R$ 100 e R$ 200 para evitar que o caixa fique apenas com troco pequeno.

O saque só é realizado se o valor exato puder ser composto com o estoque atual. Quando o caixa possui o valor, mas não consegue montá-lo com as cédulas disponíveis, o sistema informa o erro e sugere os valores possíveis mais próximos (abaixo e acima do pedido).

## Log de eventos

Todas as operações são registradas com data e hora no arquivo `eventos_caixa.log`, criado ao lado do `main.py`:

```
[27/10/2026 14:32:18] Saque REALIZADO | conta 1001 | R$ 250,00 | Menor quantidade de cédulas | 1x R$ 200,00, 1x R$ 50,00
```

Os eventos também são exibidos no console e podem ser consultados pelo menu do operador.

## Decisões de design

- **Valores em centavos (`int`):** evita os erros de arredondamento do `float`, essenciais para compor valores exatos com moedas.
- **Programação dinâmica nas estratégias:** o algoritmo guloso (pegar sempre a maior cédula) falha com estoque limitado. Exemplo: com 1x R$ 50 e 3x R$ 20, o guloso não consegue sacar R$ 60, mas a programação dinâmica encontra 3x R$ 20.
- **Conta de operador:** como toda interação deve começar pelo identificador da conta, as operações de abastecimento exigem uma conta com perfil de operador.

## Padrões e princípios aplicados

- **Strategy:** estratégias de composição intercambiáveis, recebidas pelo serviço de saque no momento da chamada.
- **Template Method:** as duas estratégias compartilham o algoritmo e definem apenas o critério de escolha.
- **Observer:** um ou mais notificadores são registrados e avisados a cada evento.
- **Facade:** `CaixaEletronico` centraliza as operações e a validação da conta.
- **Aberto/Fechado (SOLID):** novas denominações, estratégias ou notificadores são adicionados sem modificar o código existente.
- **Inversão de Dependência (SOLID):** o serviço de saque depende do contrato da estratégia, não das implementações.

## Exemplo: valor indisponível para composição

1. Entre como `admin` e descarregue as 50 moedas de R$ 1.
2. Entre como `1001` e tente sacar R$ 3.
3. O caixa recusa o saque e sugere R$ 2 e R$ 4.
