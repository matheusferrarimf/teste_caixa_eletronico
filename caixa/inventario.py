from caixa.dinheiro import Composicao, Denominacao
from caixa.excecoes import EstoqueInsuficienteError


class InventarioCaixa:
    """Controla quantas unidades existem de cada denominação."""

    def __init__(self) -> None:
        self._estoque: Composicao = {}

    def carregar(self, denominacao: Denominacao, quantidade: int) -> None:
        self._validar_quantidade(quantidade)
        self._estoque[denominacao] = self.quantidade(denominacao) + quantidade

    def descarregar(self, denominacao: Denominacao, quantidade: int) -> None:
        self._validar_quantidade(quantidade)
        disponivel = self.quantidade(denominacao)
        if quantidade > disponivel:
            raise EstoqueInsuficienteError(
                f"Há apenas {disponivel} unidade(s) de {denominacao} no caixa.")
        self._estoque[denominacao] = disponivel - quantidade

    def descarregar_composicao(self, composicao: Composicao) -> None:
        """Valida tudo antes de alterar qualquer coisa."""
        for denominacao, quantidade in composicao.items():
            if quantidade > self.quantidade(denominacao):
                raise EstoqueInsuficienteError(f"Estoque insuficiente de {denominacao}.")
        for denominacao, quantidade in composicao.items():
            self.descarregar(denominacao, quantidade)

    def quantidade(self, denominacao: Denominacao) -> int:
        return self._estoque.get(denominacao, 0)

    def consultar_estoque(self) -> Composicao:
        """Devolve uma cópia ordenada (maior → menor), sem as zeradas."""
        return {d: q for d, q in sorted(self._estoque.items(), reverse=True) if q > 0}

    def valor_total(self) -> int:
        return sum(d.valor_centavos * q for d, q in self._estoque.items())

    @staticmethod
    def _validar_quantidade(quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")