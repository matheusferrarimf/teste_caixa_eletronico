from caixa.dinheiro import formatar_reais
from caixa.excecoes import ContaNaoEncontradaError, SaldoInsuficienteError


class Conta:
    def __init__(self, identificador: str, saldo_centavos: int = 0, operador: bool = False):
        if saldo_centavos < 0:
            raise ValueError("O saldo inicial não pode ser negativo.")
        self._identificador = identificador
        self._saldo_centavos = saldo_centavos
        self._operador = operador

    @property
    def identificador(self) -> str:
        return self._identificador

    @property
    def saldo(self) -> int:
        return self._saldo_centavos

    @property
    def eh_operador(self) -> bool:
        return self._operador

    def verificar_saldo(self, valor_centavos: int) -> None:
        if valor_centavos > self._saldo_centavos:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente. Disponível: {formatar_reais(self._saldo_centavos)}.")

    def debitar(self, valor_centavos: int) -> None:
        self.verificar_saldo(valor_centavos)
        self._saldo_centavos -= valor_centavos


class RepositorioContas:
    def __init__(self) -> None:
        self._contas: dict[str, Conta] = {}

    def adicionar(self, conta: Conta) -> None:
        if conta.identificador in self._contas:
            raise ValueError(f"Já existe uma conta com o identificador {conta.identificador}.")
        self._contas[conta.identificador] = conta

    def buscar(self, identificador: str) -> Conta:
        conta = self._contas.get(identificador)
        if conta is None:
            raise ContaNaoEncontradaError(f"Conta '{identificador}' não encontrada.")
        return conta