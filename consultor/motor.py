"""Base de conhecimento + motor de inferência (Experta).

Arquitetura (mapeada para a Aula 8):

    Base de Conhecimento  -> as regras @Rule desta classe (25 regras de domínio)
    Motor de Inferência   -> o Experta (encadeamento para frente / forward chaining)
    Memória de Trabalho   -> o fato `Resposta` + a pontuação acumulada
    Explicador            -> a lista `Disparo` (quais regras dispararam e por quê)

Estratégia de raciocínio (como o sistema decide):

    1. As respostas do usuário entram como UM fato (`Resposta`).
    2. Cada regra de domínio cruza 2-3 respostas. Se casar, ela soma (ou
       subtrai) pontos para uma trilha e registra o MOTIVO (justificativa).
    3. Quando todas as regras de domínio terminam, a regra `decisao_final`
       (salience menor = roda por último) lê a pontuação e escolhe a trilha.
"""

from __future__ import annotations

# ATENÇÃO: o compat PRECISA vir antes do experta (ver compat.py).
from . import compat  # noqa: F401
from dataclasses import dataclass, field

from experta import Fact, KnowledgeEngine, P, Rule

from .perguntas import validar_respostas
from .trilhas import TRILHAS

# Limiares de decisão (ajustáveis)
PONTOS_MINIMOS = 5  # abaixo disso o sistema diz "inconclusivo"
MARGEM_ALTA = 5
MARGEM_MEDIA = 2


# --------------------------------------------------------------------------
# Fatos e estruturas de resultado
# --------------------------------------------------------------------------
class Resposta(Fact):
    """Um fato com todas as respostas da entrevista (slots = chaves de PERGUNTAS)."""


@dataclass(frozen=True)
class Disparo:
    """Registro de uma regra que disparou (a base da justificativa)."""

    regra: str
    trilha: str
    pontos: int
    motivo: str


@dataclass
class Resultado:
    trilha: str | None  # None quando inconclusivo
    pontuacao: dict[str, int]
    ranking: list[tuple[str, int]]
    disparos: list[Disparo] = field(default_factory=list)
    confianca: str = "inconclusiva"  # alta | media | baixa | inconclusiva
    empate: list[str] = field(default_factory=list)

    @property
    def motivos_da_vencedora(self) -> list[Disparo]:
        if self.trilha is None:
            return []
        return sorted(
            (d for d in self.disparos if d.trilha == self.trilha),
            key=lambda d: -d.pontos,
        )


def uma_de(*valores: str):
    """Padrão do Experta: o slot precisa valer um dos `valores` (um "OU")."""
    return P(lambda v: v in valores)


# --------------------------------------------------------------------------
# O motor
# --------------------------------------------------------------------------
class ConsultorCarreiras(KnowledgeEngine):
    def __init__(self) -> None:
        super().__init__()
        self.pontuacao: dict[str, int] = {t: 0 for t in TRILHAS}
        self.disparos: list[Disparo] = []
        self.resultado: Resultado | None = None

    def _pontuar(self, regra: str, trilha: str, pontos: int, motivo: str) -> None:
        self.pontuacao[trilha] += pontos
        self.disparos.append(Disparo(regra, trilha, pontos, motivo))

    # ===================== DECISÃO =======================================
    # salience negativa = roda DEPOIS de todas as regras de domínio (salience 0).
    @Rule(Resposta(), salience=-100)
    def decisao_final(self):
        # Ordena por pontos (desc); empate cai na ordem de TRILHAS (estável).
        ranking = sorted(self.pontuacao.items(), key=lambda kv: -kv[1])
        (lider, p1), (_, p2) = ranking[0], ranking[1]
        empatadas = [t for t, p in ranking if p == p1] if p1 > 0 else []

        if p1 < PONTOS_MINIMOS:
            trilha, confianca = None, "inconclusiva"
        else:
            trilha = lider
            margem = p1 - p2
            if margem >= MARGEM_ALTA:
                confianca = "alta"
            elif margem >= MARGEM_MEDIA:
                confianca = "media"
            else:
                confianca = "baixa"

        self.resultado = Resultado(
            trilha=trilha,
            pontuacao=dict(self.pontuacao),
            ranking=ranking,
            disparos=list(self.disparos),
            confianca=confianca,
            empate=empatadas if len(empatadas) > 1 else [],
        )


# --------------------------------------------------------------------------
# API simples para a interface e para os testes
# --------------------------------------------------------------------------
def recomendar(respostas: dict[str, str]) -> Resultado:
    """Roda uma consulta completa e devolve o `Resultado`.

    Cria um motor NOVO a cada chamada: o Experta guarda estado (fatos, agenda),
    então reutilizar o mesmo objeto misturaria consultas diferentes.
    """
    validar_respostas(respostas)
    motor = ConsultorCarreiras()
    motor.reset()  # limpa a memória de trabalho (sempre antes de declarar fatos)
    motor.declare(Resposta(**respostas))
    motor.run()  # dispara as regras até a agenda esvaziar
    assert motor.resultado is not None, "decisao_final não disparou"
    return motor.resultado
