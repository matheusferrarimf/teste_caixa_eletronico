class ErroCaixaEletronico(Exception):
    """Base de todos os erros de negócio do caixa."""

class ContaNaoEncontradaError(ErroCaixaEletronico): pass
class OperacaoNaoPermitidaError(ErroCaixaEletronico): pass
class SaldoInsuficienteError(ErroCaixaEletronico): pass
class EstoqueInsuficienteError(ErroCaixaEletronico): pass


class ComposicaoImpossivelError(ErroCaixaEletronico):
    """Questão 4: o caixa tem o valor, mas não consegue montá-lo com as cédulas atuais."""
    def __init__(self, mensagem: str, sugestoes: list[int]):
        super().__init__(mensagem)
        self.sugestoes = sugestoes