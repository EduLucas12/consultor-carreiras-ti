"""Mostra, passo a passo, quais regras o Experta dispara (e em que ordem).

Uso:  python scripts/depurar.py            # usa a 1ª persona
      python scripts/depurar.py "Bruno"    # persona cujo nome começa com "Bruno"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from consultor import compat  # noqa: F401,E402  (antes do experta!)
from experta.watchers import watch  # noqa: E402

from consultor.motor import ConsultorCarreiras, Resposta  # noqa: E402
from consultor.personas import PERSONAS  # noqa: E402

prefixo = sys.argv[1] if len(sys.argv) > 1 else PERSONAS[0].nome
persona = next(p for p in PERSONAS if p.nome.startswith(prefixo))

print(f"Persona: {persona.nome}\n{persona.descricao}\n")
watch("RULES")  # outras opções: "FACTS", "AGENDA", "ACTIVATIONS"

motor = ConsultorCarreiras()
motor.reset()
motor.declare(Resposta(**persona.respostas))
motor.run()

r = motor.resultado
print(f"\nTrilha: {r.trilha} | confiança: {r.confianca}")
for d in r.motivos_da_vencedora:
    print(f"  {d.regra} ({d.pontos:+d}) {d.motivo}")
