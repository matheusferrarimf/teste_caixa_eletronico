# tests/test_estrategias.py
import unittest
from caixa.dinheiro import Denominacao
from caixa.estrategias import EstrategiaMenorQuantidade, EstrategiaPreservarMaiores


def reais(valor: int) -> Denominacao:
    return Denominacao(valor * 100)


class TestEstrategias(unittest.TestCase):
    def test_menor_quantidade_resolve_caso_em_que_o_guloso_falha(self):
        estoque = {reais(50): 1, reais(20): 3}
        self.assertEqual(EstrategiaMenorQuantidade().compor(6000, estoque), {reais(20): 3})

    def test_preservar_maiores_usa_cedulas_pequenas(self):
        estoque = {reais(100): 2, reais(50): 2, reais(20): 5}
        self.assertEqual(EstrategiaPreservarMaiores().compor(10000, estoque), {reais(20): 5})

    def test_retorna_none_quando_nao_ha_composicao(self):
        self.assertIsNone(EstrategiaMenorQuantidade().compor(300, {reais(2): 10}))