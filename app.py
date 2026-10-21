"""Interface web (Streamlit) do Consultor Inteligente de Carreiras em TI.

Rodar:  streamlit run app.py

Conceito-chave do Streamlit: o script INTEIRO é reexecutado a cada interação
(clique, seleção...). Por isso o resultado fica em `st.session_state`: sem isso
ele desapareceria no próximo rerun.
"""

import pandas as pd
import streamlit as st

from consultor.motor import recomendar
from consultor.perguntas import PERGUNTAS
from consultor.personas import PERSONAS
from consultor.trilhas import TRILHAS

st.set_page_config(page_title="Consultor de Carreiras em TI", page_icon="🧭", layout="centered")

NENHUMA = "— escolher —"
CONFIANCA_TEXTO = {
    "alta": "🟢 Confiança alta",
    "media": "🟡 Confiança média: há uma trilha concorrente próxima",
    "baixa": "🟠 Confiança baixa: duas trilhas quase empatadas",
}


# --------------------------------------------------------------------------
# Personas (atalho para demonstração e testes manuais)
# --------------------------------------------------------------------------
def aplicar_persona() -> None:
    """Callback do seletor: preenche as respostas com as de uma persona."""
    escolhida = st.session_state["persona_sel"]
    persona = next((p for p in PERSONAS if p.nome == escolhida), None)
    for p in PERGUNTAS:
        st.session_state[f"q_{p.chave}"] = persona.respostas[p.chave] if persona else None
    st.session_state.pop("resultado", None)


with st.sidebar:
    st.header("🧪 Modo demonstração")
    st.selectbox(
        "Carregar uma persona de teste",
        [NENHUMA] + [p.nome for p in PERSONAS],
        key="persona_sel",
        on_change=aplicar_persona,
    )
    st.caption("Preenche o formulário com um perfil fictício para você ver o sistema funcionando.")
    st.divider()
    st.caption(
        "Sistema especialista baseado em regras: **25 regras SE-ENTÃO** (Experta) com "
        "encadeamento para frente. Projeto da disciplina de Inteligência Artificial - UNIPAC Barbacena."
    )

# --------------------------------------------------------------------------
# Entrevista
# --------------------------------------------------------------------------
st.title("🧭 Consultor Inteligente de Carreiras em TI")
st.write("Responda às perguntas abaixo e o sistema recomenda a trilha mais adequada e **explica o porquê**.")

respostas: dict[str, str | None] = {}
for i, p in enumerate(PERGUNTAS, start=1):
    respostas[p.chave] = st.radio(
        f"{i}. {p.titulo}",
        options=list(p.opcoes),
        format_func=lambda valor, p=p: p.opcoes[valor],
        index=None,
        key=f"q_{p.chave}",
    )

if st.button("Descobrir minha trilha", type="primary"):
    faltando = [str(i) for i, p in enumerate(PERGUNTAS, 1) if respostas[p.chave] is None]
    if faltando:
        st.session_state.pop("resultado", None)
        st.warning(f"Responda todas as perguntas. Faltam: {', '.join(faltando)}.")
    else:
        st.session_state["resultado"] = recomendar(respostas)

# --------------------------------------------------------------------------
# Resultado + justificativa (módulo Explicador)
# --------------------------------------------------------------------------
resultado = st.session_state.get("resultado")
if resultado:
    st.divider()
    if resultado.trilha is None:
        st.info(
            "🤔 **Resultado inconclusivo.** Suas respostas não ativaram regras suficientes para "
            "uma recomendação segura. Veja as trilhas mais próximas abaixo ou refaça a entrevista "
            "com respostas mais específicas."
        )
    else:
        trilha = TRILHAS[resultado.trilha]
        st.success(f"### Trilha recomendada: {trilha.nome}")
        st.write(trilha.foco)
        st.caption(CONFIANCA_TEXTO.get(resultado.confianca, ""))
        if resultado.empate:
            nomes = " e ".join(TRILHAS[t].nome for t in resultado.empate)
            st.warning(f"Empate técnico entre: {nomes}. Considere explorar as duas.")

        st.subheader("Por que essa trilha? (regras disparadas)")
        for d in resultado.motivos_da_vencedora:
            sinal = "+" if d.pontos > 0 else ""
            st.markdown(f"**{d.regra}** · `{sinal}{d.pontos} pts` — {d.motivo}")

        st.subheader("Por onde começar")
        for passo in trilha.comecar_por:
            st.markdown(f"- {passo}")

    st.subheader("Ranking das trilhas")
    top3 = [(t, p) for t, p in resultado.ranking[:3]]
    colunas = st.columns(3)
    for col, (tid, pts) in zip(colunas, top3):
        col.metric(TRILHAS[tid].nome, f"{pts} pts")

    df = pd.DataFrame(
        {"Trilha": [TRILHAS[t].nome for t, _ in resultado.ranking],
         "Pontos": [p for _, p in resultado.ranking]}
    ).set_index("Trilha")
    st.bar_chart(df)

    with st.expander("Ver todas as regras disparadas (rastro completo do raciocínio)"):
        if resultado.disparos:
            st.dataframe(
                pd.DataFrame(
                    [
                        {"Regra": d.regra, "Trilha": TRILHAS[d.trilha].nome,
                         "Pontos": d.pontos, "Motivo": d.motivo}
                        for d in sorted(resultado.disparos, key=lambda d: d.regra)
                    ]
                ),
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.write("Nenhuma regra de domínio disparou.")
