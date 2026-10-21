"""Fase 4: validação com personas de teste."""

import pytest

from consultor.motor import recomendar
from consultor.personas import PERSONA_INDECISA, PERSONAS


def test_enunciado_exige_pelo_menos_4_personas_distintas():
    assert sum(p.exigida for p in PERSONAS) >= 4
    assert len({p.esperado for p in PERSONAS}) >= 4


@pytest.mark.parametrize("persona", PERSONAS, ids=lambda p: p.nome)
def test_sistema_acerta_a_trilha_esperada(persona):
    r = recomendar(persona.respostas)
    assert r.trilha == persona.esperado, f"ranking: {r.ranking[:3]}"
    assert r.confianca in ("alta", "media"), "acerto com empate técnico é frágil"
    assert not r.empate


def test_todas_as_10_trilhas_tem_persona():
    from consultor.trilhas import TRILHAS

    assert {p.esperado for p in PERSONAS} == set(TRILHAS)


def test_perfil_sem_sinais_claros_e_inconclusivo():
    r = recomendar(PERSONA_INDECISA)
    assert r.trilha is None
    assert r.confianca == "inconclusiva"


def test_cientista_x_engenheiro_de_dados_so_muda_o_foco():
    """O caso que o enunciado pede para diferenciar com precisão."""
    base = dict(matematica="media", atuacao="dados_brutos", ferramenta="python",
                entrega="insights", foco_infra="nenhum", plataforma="indiferente", social="baixo")
    cientista = recomendar({**base, "matematica": "alta", "foco_dados": "modelos"})
    engenheiro = recomendar({**base, "foco_dados": "pipelines"})
    assert cientista.trilha == "ciencia_dados"
    assert engenheiro.trilha == "engenharia_dados"


def test_devops_x_cloud_so_muda_o_foco_de_infra():
    base = dict(matematica="media", atuacao="servidores", ferramenta="linux_redes",
                entrega="infraestrutura", foco_dados="nenhum", plataforma="indiferente", social="medio")
    assert recomendar({**base, "foco_infra": "nuvem"}).trilha == "cloud"
    assert recomendar({**base, "foco_infra": "ci_cd"}).trilha == "devops"


def test_frontend_x_mobile_depende_da_plataforma():
    base = dict(matematica="media", atuacao="layouts", ferramenta="javascript",
                entrega="produto_final", foco_dados="nenhum", foco_infra="nenhum", social="medio")
    assert recomendar({**base, "plataforma": "web"}).trilha == "frontend"
    assert recomendar({**base, "plataforma": "celular"}).trilha == "mobile"
