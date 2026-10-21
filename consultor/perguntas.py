"""A entrevista: perguntas e respostas válidas.

Este arquivo é o "vocabulário" do sistema (é a mini-ontologia
do domínio). O motor de regras e a interface leem DAQUI, então os valores
usados nas regras (ex.: "python", "layouts") nunca ficam fora de sincronia.

As 4 primeiras perguntas são as exigidas no enunciado. As 4 últimas foram
acrescentadas porque 4 dimensões não bastam para separar 10 trilhas
(ex.: Ciência x Engenharia de Dados, DevOps x Cloud).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Pergunta:
    chave: str  # nome do slot do Fact (ex.: "matematica")
    titulo: str  # texto mostrado ao usuário
    opcoes: dict[str, str]  # valor interno -> rótulo mostrado


PERGUNTAS: tuple[Pergunta, ...] = (
    # ---- Dimensões exigidas no enunciado -------------------------------
    Pergunta(
        "matematica",
        "Qual é a sua afinidade com matemática e estatística?",
        {"baixa": "Baixa", "media": "Média", "alta": "Alta"},
    ),
    Pergunta(
        "atuacao",
        "O que você mais gostaria de fazer no dia a dia de trabalho?",
        {
            "algoritmos": "Escrever algoritmos e regras lógicas",
            "layouts": "Criar layouts e interfaces visuais",
            "servidores": "Configurar e manter servidores, redes e ambientes",
            "dados_brutos": "Analisar dados brutos",
            "seguranca": "Garantir segurança / encontrar falhas",
            "automacao": "Automatizar processos de build e entrega",
            "testes": "Testar software e caçar bugs",
            "negocio": "Conversar com clientes e decidir o que construir",
        },
    ),
    Pergunta(
        "ferramenta",
        "Qual linguagem/ferramenta você domina melhor hoje?",
        {
            "python": "Python",
            "javascript": "JavaScript",
            "sql": "SQL / bancos de dados",
            "linux_redes": "Linux / Redes",
            "mobile_lang": "Kotlin / Swift / Dart / Java (mobile)",
            "nenhuma": "Nenhuma / estou iniciando",
        },
    ),
    Pergunta(
        "entrega",
        "Que tipo de valor você prefere entregar?",
        {
            "produto_final": "O produto final que o usuário usa",
            "infraestrutura": "A infraestrutura que sustenta o sistema",
            "seguranca": "A segurança contra invasões",
            "insights": "Informações e previsões para apoiar decisões",
            "qualidade": "A confiabilidade e a qualidade do software",
            "valor_negocio": "Resultado para o negócio e para o cliente",
        },
    ),
    # ---- Dimensões extras (desambiguação) -------------------------------
    Pergunta(
        "foco_dados",
        "Se trabalhasse com dados, o que mais te atrairia?",
        {
            "modelos": "Criar modelos, previsões e experimentos estatísticos",
            "pipelines": "Construir pipelines e a arquitetura que movimenta os dados",
            "nenhum": "Não tenho interesse em trabalhar com dados",
        },
    ),
    Pergunta(
        "foco_infra",
        "Se trabalhasse com infraestrutura, o que mais te atrairia?",
        {
            "nuvem": "Projetar arquiteturas e custos em provedores de nuvem (AWS/Azure/GCP)",
            "ci_cd": "Automatizar CI/CD, contêineres e monitoramento",
            "nenhum": "Não tenho interesse em infraestrutura",
        },
    ),
    Pergunta(
        "plataforma",
        "Para qual plataforma você prefere construir?",
        {
            "web": "Web",
            "celular": "Aplicativos de celular",
            "indiferente": "Tanto faz / não se aplica",
        },
    ),
    Pergunta(
        "social",
        "Quanto você gosta de interagir com pessoas, clientes e decisões de negócio?",
        {"baixo": "Prefiro focar sozinho", "medio": "Moderadamente", "alto": "Muito"},
    ),
)

CHAVES = tuple(p.chave for p in PERGUNTAS)


def validar_respostas(respostas: dict) -> None:
    """Levanta ValueError se faltar resposta ou houver valor desconhecido."""
    for p in PERGUNTAS:
        if p.chave not in respostas or respostas[p.chave] is None:
            raise ValueError(f"Resposta ausente: '{p.chave}'")
        if respostas[p.chave] not in p.opcoes:
            raise ValueError(
                f"Valor inválido para '{p.chave}': {respostas[p.chave]!r}. "
                f"Válidos: {list(p.opcoes)}"
            )
    extras = set(respostas) - set(CHAVES)
    if extras:
        raise ValueError(f"Chaves desconhecidas: {sorted(extras)}")
