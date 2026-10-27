from caixa.dinheiro import Composicao


def valores_sacaveis(estoque: Composicao, limite_centavos: int) -> set[int]:
    """Todos os valores exatos que o estoque consegue montar, até o limite."""
    alcancaveis = {0}
    for denominacao, disponivel in estoque.items():
        novos = set(alcancaveis)
        for subtotal in alcancaveis:
            for qtd in range(1, disponivel + 1):
                valor = subtotal + qtd * denominacao.valor_centavos
                if valor > limite_centavos:
                    break
                novos.add(valor)
        alcancaveis = novos
    alcancaveis.discard(0)
    return alcancaveis


def sugerir_valores(valor_pedido: int, estoque: Composicao, teto: int) -> list[int]:
    """O valor sacável imediatamente abaixo e acima do pedido."""
    if not estoque:
        return []
    maior_cedula = max(d.valor_centavos for d in estoque)
    possiveis = valores_sacaveis(estoque, min(teto, valor_pedido + maior_cedula))
    abaixo = [v for v in possiveis if v < valor_pedido]
    acima = [v for v in possiveis if v > valor_pedido]
    return ([max(abaixo)] if abaixo else []) + ([min(acima)] if acima else [])