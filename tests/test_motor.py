"""Testes da base de conhecimento e do motor de inferência."""

import re
from pathlib import Path

import pytest
from experta import Rule

from consultor.motor import ConsultorCarreiras, recomendar
from consultor.perguntas import PERGUNTAS
from consultor.personas import PERSONAS

RAIZ = Path(__file__).resolve().parent.parent
PADRAO_REGRA = re.compile(r"^r(\d{2})_")


def _regras_de_dominio() -> list[str]:
    return sorted(
        nome
        for nome, valor in vars(ConsultorCarreiras).items()
        if isinstance(valor, Rule) and PADRAO_REGRA.match(nome)
    )


def test_base_tem_entre_20_e_25_regras_de_dominio():
    assert 20 <= len(_regras_de_dominio()) <= 25


def test_ids_das_regras_sao_sequenciais():
    ids = [int(PADRAO_REGRA.match(n).group(1)) for n in _regras_de_dominio()]
    assert ids == list(range(1, len(ids) + 1))


def test_toda_regra_aparece_na_matriz_de_decisao():
    """Garante que a documentação (Fase 1) não ficou para trás do código."""
    matriz = (RAIZ / "docs" / "matriz_decisao.md").read_text(encoding="utf-8")
    for n in _regras_de_dominio():
        rid = f"R{PADRAO_REGRA.match(n).group(1)}"
        assert rid in matriz, f"{rid} não está em docs/matriz_decisao.md"


def test_toda_regra_dispara_em_algum_caso():
    """Nenhuma regra morta: cada uma precisa disparar para alguma combinação."""
    import itertools
    import random

    espaco = list(itertools.product(*[list(p.opcoes) for p in PERGUNTAS]))
    random.Random(7).shuffle(espaco)
    chaves = [p.chave for p in PERGUNTAS]
    dispararam = set()
    for combo in espaco[:1500]:
        dispararam |= {d.regra for d in recomendar(dict(zip(chaves, combo))).disparos}
    for p in PERSONAS:
        dispararam |= {d.regra for d in recomendar(p.respostas).disparos}
    esperadas = {f"R{PADRAO_REGRA.match(n).group(1)}" for n in _regras_de_dominio()}
    assert esperadas <= dispararam, f"regras mortas: {sorted(esperadas - dispararam)}"


def test_justificativa_cita_regras_da_trilha_vencedora():
    persona = PERSONAS[0]
    r = recomendar(persona.respostas)
    motivos = r.motivos_da_vencedora
    assert motivos, "toda recomendação precisa de justificativa"
    assert all(d.trilha == r.trilha for d in motivos)
    assert sum(d.pontos for d in motivos) == r.pontuacao[r.trilha]


def test_consultas_nao_vazam_estado_entre_si():
    a = recomendar(PERSONAS[0].respostas)
    b = recomendar(PERSONAS[1].respostas)
    a2 = recomendar(PERSONAS[0].respostas)
    assert a.pontuacao == a2.pontuacao
    assert a.trilha != b.trilha


def test_regra_de_decisao_roda_por_ultimo():
    """salience=-100 faz `decisao_final` olhar a pontuação já completa."""
    r = recomendar(PERSONAS[0].respostas)
    assert r.ranking[0][1] == max(r.pontuacao.values())


@pytest.mark.parametrize(
    "mudanca",
    [{"matematica": "extrema"}, {"atuacao": None}, {"foco_dados": "xyz"}],
)
def test_respostas_invalidas_sao_rejeitadas(mudanca):
    ok = dict(PERSONAS[0].respostas)
    with pytest.raises(ValueError):
        recomendar({**ok, **mudanca})


def test_resposta_faltando_e_rejeitada():
    ok = dict(PERSONAS[0].respostas)
    ok.pop("social")
    with pytest.raises(ValueError):
        recomendar(ok)
