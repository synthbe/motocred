# type_aliases.py
from typing import Dict, Any, Literal, TypeAlias, List, Tuple

Report: TypeAlias = Dict[str, list[dict[str, Any]]]

AnalysiResult: TypeAlias = Literal[
    "SCORE NÂO CALULADO",
    "REPROVADO POR SCORE",
    "REPROVADO POR QUANTIDADE DE NEGATIVACOES E DIVIDAS",
    "REPROVADO POR VALOR DAS NEGATIVACOES E DIVIDAS",
    "PRE APROVADO"
]

CustomerDataLoan: TypeAlias = Dict[str, str | float | Tuple[float, float, float]]

SheetBody: TypeAlias = Dict[str, List[List[str | int | float]]]
