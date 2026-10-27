from caixa.contas import Conta, RepositorioContas
from caixa.dinheiro import Composicao, Denominacao, descrever_composicao, formatar_reais
from caixa.estrategias import EstrategiaComposicao
from caixa.excecoes import ErroCaixaEletronico, OperacaoNaoPermitidaError
from caixa.inventario import InventarioCaixa
from caixa.notificacao import Notificador
from caixa.servico_saque import ServicoSaque


class CaixaEletronico:
    def __init__(self, inventario: InventarioCaixa, contas: RepositorioContas,
                 servico_saque: ServicoSaque) -> None:
        self._inventario = inventario
        self._contas = contas
        self._servico_saque = servico_saque
        self._notificadores: list[Notificador] = []

    def registrar_notificador(self, notificador: Notificador) -> None:
        self._notificadores.append(notificador)

    def autenticar(self, id_conta: str) -> Conta:
        conta = self._contas.buscar(id_conta)
        self._notificar(f"Conta {id_conta} autenticada.")
        return conta

    def consultar_saldo(self, id_conta: str) -> int:
        conta = self._contas.buscar(id_conta)
        self._notificar(f"Conta {id_conta} consultou o saldo.")
        return conta.saldo

    def sacar(self, id_conta: str, valor_centavos: int,
              estrategia: EstrategiaComposicao) -> Composicao:
        conta = self._contas.buscar(id_conta)
        try:
            conta.verificar_saldo(valor_centavos)
            composicao = self._servico_saque.sacar(
                valor_centavos, estrategia, teto_sugestao=conta.saldo)
        except ErroCaixaEletronico as erro:
            self._notificar(f"Saque NEGADO | conta {id_conta} | "
                            f"{formatar_reais(valor_centavos)} | {erro}")
            raise
        conta.debitar(valor_centavos)
        self._notificar(f"Saque REALIZADO | conta {id_conta} | {formatar_reais(valor_centavos)} "
                        f"| {estrategia.nome} | {descrever_composicao(composicao)}")
        return composicao

    def carregar(self, id_conta: str, denominacao: Denominacao, quantidade: int) -> None:
        self._exigir_operador(id_conta)
        self._inventario.carregar(denominacao, quantidade)
        self._notificar(f"Carga | operador {id_conta} | {quantidade}x {denominacao}")

    def descarregar(self, id_conta: str, denominacao: Denominacao, quantidade: int) -> None:
        self._exigir_operador(id_conta)
        self._inventario.descarregar(denominacao, quantidade)
        self._notificar(f"Descarga | operador {id_conta} | {quantidade}x {denominacao}")

    def consultar_estoque(self, id_conta: str) -> tuple[Composicao, int]:
        self._exigir_operador(id_conta)
        return self._inventario.consultar_estoque(), self._inventario.valor_total()

    def _exigir_operador(self, id_conta: str) -> None:
        if not self._contas.buscar(id_conta).eh_operador:
            raise OperacaoNaoPermitidaError("Operação restrita a contas de operador.")

    def _notificar(self, mensagem: str) -> None:
        for notificador in self._notificadores:
            notificador.notificar(mensagem)