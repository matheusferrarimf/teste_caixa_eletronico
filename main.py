"""Interface de console do caixa eletrônico."""
import caixa
from caixa.caixa_eletronico import CaixaEletronico
from caixa.contas import Conta, RepositorioContas
from caixa.dinheiro import (Denominacao, TipoDinheiro, converter_para_centavos,
                            descrever_composicao, formatar_reais)
from caixa.estrategias import EstrategiaMenorQuantidade, EstrategiaPreservarMaiores
from caixa.excecoes import ComposicaoImpossivelError, ErroCaixaEletronico
from caixa.inventario import InventarioCaixa
from caixa.notificacao import NotificadorArquivo, NotificadorConsole
from caixa.servico_saque import ServicoSaque


ESTOQUE_INICIAL = {
    Denominacao(20000): 5,
    Denominacao(10000): 10,
    Denominacao(5000): 10,
    Denominacao(2000): 20,
    Denominacao(1000): 20,
    Denominacao(500): 20,
    Denominacao(200): 30,
    Denominacao(100, TipoDinheiro.MOEDA): 50,
}

ESTRATEGIAS = {"1": EstrategiaMenorQuantidade(), "2": EstrategiaPreservarMaiores()}


def montar_caixa() -> CaixaEletronico:
    inventario = InventarioCaixa()
    for denominacao, quantidade in ESTOQUE_INICIAL.items():
        inventario.carregar(denominacao, quantidade)

    contas = RepositorioContas()
    contas.adicionar(Conta("1001", saldo_centavos=250_000))
    contas.adicionar(Conta("1002", saldo_centavos=8_000))
    contas.adicionar(Conta("admin", operador=True))

    caixa = CaixaEletronico(inventario, contas, ServicoSaque(inventario))

    notificador_arquivo = NotificadorArquivo("eventos_caixa.log")
    caixa.registrar_notificador(notificador_arquivo)
    caixa.registrar_notificador(NotificadorConsole())

    return caixa, notificador_arquivo
    

def fluxo_saque(caixa: CaixaEletronico, id_conta: str) -> None:
    valor = converter_para_centavos(input("Valor do saque: R$ "))
    print("Estratégia: [1] Menor quantidade de cédulas  [2] Preservar cédulas grandes")
    estrategia = ESTRATEGIAS.get(input("> ").strip(), ESTRATEGIAS["1"])
    try:
        composicao = caixa.sacar(id_conta, valor, estrategia)
        print(f"✔ Retire seu dinheiro: {descrever_composicao(composicao)}")
    except ComposicaoImpossivelError as erro:
        print(f"✖ {erro}")
        for sugestao in erro.sugestoes:
            print(f"  → Você pode sacar {formatar_reais(sugestao)}")


def ler_denominacao() -> Denominacao:
    valor = converter_para_centavos(input("Valor da cédula/moeda: R$ "))
    eh_moeda = input("É moeda? (s/N): ").strip().lower() == "s"
    return Denominacao(valor, TipoDinheiro.MOEDA if eh_moeda else TipoDinheiro.CEDULA)


def exibir_estoque(caixa: CaixaEletronico, id_conta: str) -> None:
    estoque, total = caixa.consultar_estoque(id_conta)
    for denominacao, quantidade in estoque.items():
        print(f"  {str(denominacao):<22} x {quantidade}")
    print(f"  Total disponível: {formatar_reais(total)}")


def executar_menu(titulo: str, opcoes: dict) -> None:
    """Loop genérico: opcoes = {"1": ("Descrição", função)}."""
    while True:
        print(f"\n== {titulo} ==")
        for chave, (descricao, _) in opcoes.items():
            print(f"[{chave}] {descricao}")
        print("[0] Sair")
        escolha = input("> ").strip()
        if escolha == "0":
            return
        if escolha not in opcoes:
            print("Opção inválida.")
            continue
        try:
            opcoes[escolha][1]()
        except (ErroCaixaEletronico, ValueError) as erro:
            print(f"✖ {erro}")


def main() -> None:
    caixa, notificador_arquivo = montar_caixa()
    while True:
        id_conta = input("\nInforme o identificador da conta (ou 'sair'): ").strip()
        if id_conta.lower() == "sair":
            break
        try:
            conta = caixa.autenticar(id_conta)
        except ErroCaixaEletronico as erro:
            print(f"✖ {erro}")
            continue

        if conta.eh_operador:
            executar_menu("Operador", {
                "1": ("Consultar estoque", lambda: exibir_estoque(caixa, id_conta)),
                "2": ("Carregar", lambda: caixa.carregar(
                    id_conta, ler_denominacao(), int(input("Quantidade: ")))),
                "3": ("Descarregar", lambda: caixa.descarregar(
                    id_conta, ler_denominacao(), int(input("Quantidade: ")))),
                "4": ("Ver log de eventos", lambda: print("\n".join(notificador_arquivo.ler_eventos()) or "Sem eventos.")),
            })
        else:
            executar_menu(f"Conta {id_conta}", {
                "1": ("Consultar saldo", lambda: print(
                    f"Saldo: {formatar_reais(caixa.consultar_saldo(id_conta))}")),
                "2": ("Sacar", lambda: fluxo_saque(caixa, id_conta)),
            })


if __name__ == "__main__":
    main()