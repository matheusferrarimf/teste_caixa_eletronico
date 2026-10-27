"""Tipos e utilitários de dinheiro. Todos os valores trafegam em CENTAVOS (int)."""
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from enum import Enum


class TipoDinheiro(Enum):
    CEDULA = "Cédula"
    MOEDA = "Moeda"


@dataclass(frozen=True, order=True)
class Denominacao:
    """Um valor aceito pelo caixa."""
    valor_centavos: int
    tipo: TipoDinheiro = field(default=TipoDinheiro.CEDULA, compare=False)

    def __post_init__(self):
        if self.valor_centavos <= 0:
            raise ValueError("precisa ter valor positivo.")

    def __str__(self) -> str:
        return f"{self.tipo.value} de {formatar_reais(self.valor_centavos)}"


Composicao = dict[Denominacao, int]   # denominação -> quantidade


def formatar_reais(centavos: int) -> str:
    texto = f"{centavos / 100:,.2f}"   # 1,234.50 
    return "R$ " + texto.replace(",", "_").replace(".", ",").replace("_", ".")


def converter_para_centavos(texto: str) -> int:
    """Usa Decimal para não sofrer com float."""
    try:
        valor = Decimal(texto.strip().replace(",", "."))
    except InvalidOperation:
        raise ValueError(f"Valor inválido: '{texto}'.") from None
    centavos = valor * 100
    if not valor.is_finite() or centavos <= 0 or centavos != centavos.to_integral_value():
        raise ValueError("Informe um valor positivo com no máximo 2 casas decimais.")
    return int(centavos)


def descrever_composicao(composicao: Composicao) -> str:
    return ", ".join(f"{qtd}x {formatar_reais(d.valor_centavos)}"
                     for d, qtd in sorted(composicao.items(), reverse=True))