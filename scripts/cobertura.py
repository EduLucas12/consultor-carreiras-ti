"""Análise de cobertura da base de conhecimento (ferramenta de engenharia de conhecimento).

Roda o motor em milhares de combinações de respostas e mostra:
  - quantas vezes cada trilha vence (alguma trilha nunca vence? regra faltando!)
  - quantas vezes o resultado é inconclusivo ou empata
  - quais regras NUNCA disparam (regra morta = condição impossível/errada)

Uso:  python scripts/cobertura.py [amostras]
"""

import itertools
import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consultor.motor import recomendar  # noqa: E402
from consultor.perguntas import PERGUNTAS  # noqa: E402
from consultor.trilhas import TRILHAS  # noqa: E402


def main(amostras: int) -> None:
    espaco = list(itertools.product(*[list(p.opcoes) for p in PERGUNTAS]))
    total = len(espaco)
    random.Random(42).shuffle(espaco)
    espaco = espaco[:amostras]

    venc, regras = Counter(), Counter()
    inconclusivos = empates = 0
    for combo in espaco:
        r = recomendar(dict(zip((p.chave for p in PERGUNTAS), combo)))
        venc[r.trilha] += 1
        inconclusivos += r.trilha is None
        empates += bool(r.empate)
        for d in r.disparos:
            regras[d.regra] += 1

    print(f"Espaço total de respostas: {total:,} | analisadas: {len(espaco):,}\n")
    print("Vitórias por trilha:")
    for tid in [*TRILHAS, None]:
        nome = TRILHAS[tid].nome if tid else "(inconclusivo)"
        print(f"  {venc[tid]:>6}  {nome}")
    print(f"\nInconclusivos: {inconclusivos / len(espaco):.1%} | Empates no topo: {empates / len(espaco):.1%}")
    todas = {f"R{i:02d}" for i in range(1, 26)}
    mortas = sorted(todas - set(regras))
    print("Regras que nunca dispararam:", mortas or "nenhuma")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5000)
