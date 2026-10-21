"""Personas de teste (Fase 4): perfis fictícios com a trilha esperada.

Cada persona é um "caso de teste" do sistema especialista: se o motor não
recomendar a trilha esperada, ou a persona está mal descrita ou há uma
regra errada/faltando na base de conhecimento.

As 4 personas exigidas no enunciado (analítico, infra/segurança, visual,
negócios) estão marcadas com `exigida=True`; as demais cobrem as outras trilhas
e os pares mais fáceis de confundir (Ciência x Engenharia de Dados, DevOps x
Cloud, Front-end x Mobile).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    nome: str
    descricao: str
    respostas: dict[str, str]
    esperado: str  # id da trilha
    exigida: bool = False


PERSONAS: tuple[Persona, ...] = (
    # ---------------- as 4 exigidas pelo enunciado ----------------------
    Persona(
        "Ana, a analítica",
        "Adora estatística, passa horas explorando planilhas e quer prever o futuro com dados.",
        dict(matematica="alta", atuacao="dados_brutos", ferramenta="python", entrega="insights",
             foco_dados="modelos", foco_infra="nenhum", plataforma="indiferente", social="baixo"),
        "ciencia_dados",
        exigida=True,
    ),
    Persona(
        "Bruno, o guardião",
        "Curte Linux e redes, vive em desafios de invasão (CTF) e quer proteger sistemas.",
        dict(matematica="media", atuacao="seguranca", ferramenta="linux_redes", entrega="seguranca",
             foco_dados="nenhum", foco_infra="nenhum", plataforma="indiferente", social="baixo"),
        "ciberseguranca",
        exigida=True,
    ),
    Persona(
        "Carla, a visual",
        "Pensa em cores, tipografia e usabilidade; programa em JavaScript para ver as telas ganharem vida.",
        dict(matematica="baixa", atuacao="layouts", ferramenta="javascript", entrega="produto_final",
             foco_dados="nenhum", foco_infra="nenhum", plataforma="web", social="medio"),
        "frontend",
        exigida=True,
    ),
    Persona(
        "Diego, o estrategista",
        "Gosta de ouvir clientes, priorizar o que importa e alinhar times; não programa muito.",
        dict(matematica="baixa", atuacao="negocio", ferramenta="nenhuma", entrega="valor_negocio",
             foco_dados="nenhum", foco_infra="nenhum", plataforma="indiferente", social="alto"),
        "produto",
        exigida=True,
    ),
    # ---------------- cobrindo as outras trilhas -----------------------
    Persona(
        "Elisa, a construtora de APIs",
        "Gosta de lógica, escreve Python e SQL, quer que o sistema funcione por trás das cortinas.",
        dict(matematica="media", atuacao="algoritmos", ferramenta="python", entrega="produto_final",
             foco_dados="nenhum", foco_infra="nenhum", plataforma="web", social="baixo"),
        "backend",
    ),
    Persona(
        "Fábio, o encanador de dados",
        "Dados brutos, SQL e Python, mas prefere montar pipelines a fazer estatística avançada.",
        dict(matematica="media", atuacao="dados_brutos", ferramenta="sql", entrega="infraestrutura",
             foco_dados="pipelines", foco_infra="nenhum", plataforma="indiferente", social="baixo"),
        "engenharia_dados",
    ),
    Persona(
        "Gabi, a automatizadora",
        "Quer que todo deploy aconteça sozinho: Linux, contêineres e pipelines de CI/CD.",
        dict(matematica="media", atuacao="automacao", ferramenta="linux_redes", entrega="infraestrutura",
             foco_dados="nenhum", foco_infra="ci_cd", plataforma="indiferente", social="medio"),
        "devops",
    ),
    Persona(
        "Henrique, o arquiteto de nuvem",
        "Sonha em desenhar a arquitetura e controlar o custo de sistemas escaláveis na nuvem.",
        dict(matematica="media", atuacao="servidores", ferramenta="linux_redes", entrega="infraestrutura",
             foco_dados="nenhum", foco_infra="nuvem", plataforma="indiferente", social="medio"),
        "cloud",
    ),
    Persona(
        "Iara, a dev de apps",
        "Quer ver seu app na loja de aplicativos, usando Flutter/Dart ou Kotlin.",
        dict(matematica="media", atuacao="layouts", ferramenta="mobile_lang", entrega="produto_final",
             foco_dados="nenhum", foco_infra="nenhum", plataforma="celular", social="medio"),
        "mobile",
    ),
    Persona(
        "João, o caçador de bugs",
        "Adora quebrar sistemas para provar que funcionam e escreve testes automatizados em Python.",
        dict(matematica="media", atuacao="testes", ferramenta="python", entrega="qualidade",
             foco_dados="nenhum", foco_infra="nenhum", plataforma="indiferente", social="medio"),
        "qa",
    ),
)

# Perfil sem sinais claros: o sistema deve admitir que não sabe (inconclusivo).
PERSONA_INDECISA = dict(
    matematica="media", atuacao="algoritmos", ferramenta="nenhuma", entrega="produto_final",
    foco_dados="nenhum", foco_infra="nenhum", plataforma="indiferente", social="medio",
)
