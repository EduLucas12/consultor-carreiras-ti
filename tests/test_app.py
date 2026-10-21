"""Teste da interface Streamlit sem abrir navegador (streamlit.testing.v1.AppTest)."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

from consultor.personas import PERSONAS
from consultor.trilhas import TRILHAS

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def _abrir() -> AppTest:
    at = AppTest.from_file(APP, default_timeout=30)
    at.run()
    assert not at.exception
    return at


def _textos(at: AppTest) -> str:
    partes = [m.value for m in at.markdown] + [s.value for s in at.success]
    return "\n".join(partes)


def test_app_abre_com_oito_perguntas():
    at = _abrir()
    assert len(at.radio) == 8


def test_botao_sem_responder_avisa_o_que_falta():
    at = _abrir()
    at.button[0].click().run()
    assert at.warning, "deveria avisar que faltam respostas"
    assert not at.success


def test_persona_pelo_formulario_gera_recomendacao_e_justificativa():
    persona = next(p for p in PERSONAS if p.nome.startswith("Ana"))
    at = _abrir()
    for chave, valor in persona.respostas.items():
        at.radio(key=f"q_{chave}").set_value(valor)
    at.button[0].click().run()

    assert not at.exception
    assert TRILHAS[persona.esperado].nome in at.success[0].value
    assert "R08" in _textos(at)  # a justificativa mostra as regras disparadas


def test_seletor_de_persona_preenche_formulario():
    persona = next(p for p in PERSONAS if p.nome.startswith("Bruno"))
    at = _abrir()
    at.selectbox(key="persona_sel").select(persona.nome).run()
    for chave, valor in persona.respostas.items():
        assert at.radio(key=f"q_{chave}").value == valor
