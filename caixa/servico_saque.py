from caixa.dinheiro import Composicao, formatar_reais
from caixa.estrategias import EstrategiaComposicao
from caixa.excecoes import ComposicaoImpossivelError, EstoqueInsuficienteError
from caixa.inventario import InventarioCaixa
from caixa.sugestoes import sugerir_valores


class ServicoSaque:

    def __init__(self, inventario: InventarioCaixa) -> None:
        self._inventario = inventario

    def sacar(self, valor_centavos: int, estrategia: EstrategiaComposicao,
              teto_sugestao: int | None = None) -> Composicao:
        total_caixa = self._inventario.valor_total()
        if valor_centavos > total_caixa:
            raise EstoqueInsuficienteError("O caixa não possui dinheiro suficiente para este saque.")

        estoque = self._inventario.consultar_estoque()
        composicao = estrategia.compor(valor_centavos, estoque)

        if composicao is None:   # o valor existe no caixa, mas não fecha com as cédulas
            teto = min(teto_sugestao or total_caixa, total_caixa)
            raise ComposicaoImpossivelError(
                f"Não é possível entregar exatamente {formatar_reais(valor_centavos)} "
                f"com as cédulas disponíveis no momento.",
                sugerir_valores(valor_centavos, estoque, teto))

        self._inventario.descarregar_composicao(composicao)
        return composicao