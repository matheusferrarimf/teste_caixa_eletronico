from abc import ABC, abstractmethod
from caixa.dinheiro import Composicao


class EstrategiaComposicao(ABC):
    """CONTRATO: dado um valor e o estoque, diz quais cédulas entregar.
    Retorna None se não houver composição exata."""
    nome: str = ""

    @abstractmethod
    def compor(self, valor_centavos: int, estoque: Composicao) -> Composicao | None: ...


class EstrategiaOtimizada(EstrategiaComposicao):
    """Programação dinâmica genérica. As subclasses só definem o critério (_custo)."""

    def compor(self, valor_centavos: int, estoque: Composicao) -> Composicao | None:
        melhores: dict[int, Composicao] = {0: {}}   # subtotal -> melhor composição
        for denominacao, disponivel in estoque.items():
            proximos = dict(melhores)
            for subtotal, composicao in melhores.items():
                for qtd in range(1, disponivel + 1):
                    novo_subtotal = subtotal + qtd * denominacao.valor_centavos
                    if novo_subtotal > valor_centavos:
                        break
                    candidata = {**composicao, denominacao: qtd}
                    atual = proximos.get(novo_subtotal)
                    if atual is None or self._custo(candidata) < self._custo(atual):
                        proximos[novo_subtotal] = candidata
            melhores = proximos
        return melhores.get(valor_centavos)

    @abstractmethod
    def _custo(self, composicao: Composicao):
        """Critério de comparação entre composições. Menor é melhor."""
   


class EstrategiaMenorQuantidade(EstrategiaOtimizada):
    """Estratégia padrão: menor número total de cédulas."""
    nome = "Menor quantidade de cédulas"

    def _custo(self, composicao: Composicao):
        return sum(composicao.values())


class EstrategiaPreservarMaiores(EstrategiaOtimizada):
    """Estratégia alternativa: gasta as menores primeiro."""
    nome = "Preservar cédulas grandes"

    def _custo(self, composicao: Composicao):
        # Pares (denominação, qtd) da MAIOR para a menor. Comparando tuplas,
        # vence quem usa menos R$200; se empatar, menos R$100; e assim por diante.
        return tuple(sorted(composicao.items(), reverse=True))