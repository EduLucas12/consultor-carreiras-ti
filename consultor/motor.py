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

    # ===================== BACK-END ======================================
    @Rule(
        Resposta(
            atuacao="algoritmos",
            ferramenta=uma_de("python", "sql", "javascript", "mobile_lang"),
            foco_dados="nenhum",
            plataforma=uma_de("web", "indiferente"),
        )
    )
    def r01_backend_algoritmos_linguagem(self):
        self._pontuar(
            "R01", "backend", 6,
            "Você gosta de escrever algoritmos e regras lógicas, já programa (Python, SQL, "
            "JavaScript/Node, Java...) e não quer focar em dados analíticos nem em celular: "
            "é o núcleo do Back-end (APIs, regras de negócio, bancos).",
        )

    @Rule(
        Resposta(
            atuacao="algoritmos",
            entrega=uma_de("produto_final", "infraestrutura"),
            foco_dados="nenhum",
            plataforma=uma_de("web", "indiferente"),
        )
    )
    def r02_backend_logica_para_sustentar_sistemas(self):
        self._pontuar(
            "R02", "backend", 4,
            "Programação lógica voltada a entregar ou sustentar sistemas (e não a modelar "
            "dados) combina com o Back-end.",
        )

    # ===================== FRONT-END =====================================
    @Rule(Resposta(atuacao="layouts", ferramenta="javascript"))
    def r03_frontend_layouts_javascript(self):
        self._pontuar(
            "R03", "frontend", 7,
            "Criar layouts visuais com JavaScript é a essência do Front-end.",
        )

    @Rule(Resposta(atuacao="layouts", entrega="produto_final", plataforma="web"))
    def r04_frontend_layouts_produto_web(self):
        self._pontuar(
            "R04", "frontend", 5,
            "Você quer entregar o produto final que o usuário vê, em interfaces web.",
        )

    @Rule(Resposta(atuacao="layouts", plataforma="celular"))
    def r05_frontend_penalidade_preferencia_celular(self):
        self._pontuar(
            "R05", "frontend", -2,
            "Preferir celular em vez de web reduz a aderência ao Front-end web "
            "(regra de desambiguação Front-end x Mobile).",
        )

    # ===================== MOBILE ========================================
    @Rule(Resposta(plataforma="celular", atuacao=uma_de("layouts", "algoritmos")))
    def r06_mobile_celular_construir(self):
        self._pontuar(
            "R06", "mobile", 5,
            "Você quer construir (interfaces ou lógica) para aplicativos de celular.",
        )

    @Rule(
        Resposta(
            plataforma="celular",
            ferramenta=uma_de("mobile_lang", "javascript"),
            entrega="produto_final",
        )
    )
    def r07_mobile_ferramenta_e_produto(self):
        self._pontuar(
            "R07", "mobile", 5,
            "Sua ferramenta (Kotlin/Swift/Dart/Java ou JavaScript) e o desejo de entregar o "
            "produto final no celular apontam para Mobile (nativo ou Flutter/React Native).",
        )

    # ===================== CIÊNCIA DE DADOS ==============================
    @Rule(Resposta(matematica="alta", atuacao="dados_brutos", foco_dados="modelos"))
    def r08_ds_matematica_dados_modelos(self):
        self._pontuar(
            "R08", "ciencia_dados", 8,
            "Matemática alta + análise de dados brutos + interesse em criar modelos e previsões "
            "é o perfil central de Ciência de Dados e Machine Learning.",
        )

    @Rule(
        Resposta(entrega="insights", foco_dados="modelos", ferramenta=uma_de("python", "sql"))
    )
    def r09_ds_insights_modelos_python(self):
        self._pontuar(
            "R09", "ciencia_dados", 5,
            "Entregar previsões e informações para decisão, modelando dados com Python/SQL, "
            "é típico de Ciência de Dados.",
        )

    @Rule(Resposta(matematica="baixa", foco_dados="modelos"))
    def r10_ds_penalidade_pouca_matematica(self):
        self._pontuar(
            "R10", "ciencia_dados", -4,
            "Modelagem preditiva exige estatística: afinidade baixa com matemática reduz a "
            "aderência a Ciência de Dados.",
        )

    # ===================== ENGENHARIA DE DADOS ===========================
    @Rule(
        Resposta(
            atuacao="dados_brutos",
            foco_dados="pipelines",
            ferramenta=uma_de("python", "sql"),
        )
    )
    def r11_de_dados_brutos_pipelines(self):
        self._pontuar(
            "R11", "engenharia_dados", 8,
            "Lidar com dados brutos, construindo pipelines com Python/SQL, é o centro da "
            "Engenharia de Dados (ETL/ELT).",
        )

    @Rule(Resposta(foco_dados="pipelines", entrega="infraestrutura"))
    def r12_de_pipelines_infraestrutura(self):
        self._pontuar(
            "R12", "engenharia_dados", 5,
            "Você quer sustentar a infraestrutura por onde os dados trafegam (data lakes, "
            "pipelines).",
        )

    @Rule(
        Resposta(
            matematica=uma_de("baixa", "media"),
            atuacao="dados_brutos",
            foco_dados="pipelines",
        )
    )
    def r13_de_menos_estatistica_que_ds(self):
        self._pontuar(
            "R13", "engenharia_dados", 2,
            "Trabalhar com dados focando em arquitetura (e não em estatística avançada) "
            "diferencia o Engenheiro do Cientista de Dados.",
        )

    # ===================== CIBERSEGURANÇA ================================
    @Rule(Resposta(atuacao="seguranca", entrega="seguranca"))
    def r14_sec_atuacao_e_entrega(self):
        self._pontuar(
            "R14", "ciberseguranca", 8,
            "Você quer trabalhar com segurança e entregar proteção contra invasões: "
            "perfil direto de Cibersegurança.",
        )

    @Rule(Resposta(atuacao="seguranca", ferramenta="linux_redes"))
    def r15_sec_linux_redes(self):
        self._pontuar(
            "R15", "ciberseguranca", 5,
            "Segurança + domínio de Linux/Redes é a base para análise de vulnerabilidades "
            "e redes seguras.",
        )

    # ===================== DEVOPS & SRE ==================================
    @Rule(Resposta(atuacao="automacao", foco_infra="ci_cd"))
    def r16_devops_automacao_cicd(self):
        self._pontuar(
            "R16", "devops", 8,
            "Automatizar processos de entrega com CI/CD e contêineres é a definição de DevOps.",
        )

    @Rule(
        Resposta(
            ferramenta="linux_redes",
            foco_infra="ci_cd",
            entrega="infraestrutura",
        )
    )
    def r17_devops_linux_cicd_infra(self):
        self._pontuar(
            "R17", "devops", 5,
            "Linux/Redes, interesse em CI/CD e foco em sustentar a infraestrutura combinam "
            "com DevOps/SRE.",
        )

    @Rule(Resposta(atuacao="servidores", foco_infra="ci_cd"))
    def r18_devops_servidores_cicd(self):
        self._pontuar(
            "R18", "devops", 3,
            "Cuidar de servidores com mentalidade de automação (CI/CD) aponta para DevOps "
            "(e não para arquitetura em nuvem).",
        )

    # ===================== CLOUD =========================================
    @Rule(Resposta(foco_infra="nuvem", entrega="infraestrutura"))
    def r19_cloud_nuvem_infra(self):
        self._pontuar(
            "R19", "cloud", 7,
            "Interesse em projetar infraestrutura em provedores de nuvem e entregar a base "
            "que sustenta os sistemas: Cloud Architecture.",
        )

    @Rule(Resposta(atuacao="servidores", foco_infra="nuvem"))
    def r20_cloud_servidores_nuvem(self):
        self._pontuar(
            "R20", "cloud", 5,
            "Gerir servidores e ambientes, migrando/escalando na nuvem, é trabalho de "
            "Computação em Nuvem.",
        )

    @Rule(
        Resposta(
            atuacao=uma_de("servidores", "automacao"),
            foco_infra="nuvem",
            social=uma_de("medio", "alto"),
        )
    )
    def r21_cloud_dialoga_com_times(self):
        self._pontuar(
            "R21", "cloud", 3,
            "Arquitetos de nuvem planejam e negociam soluções (custo, escala) com times "
            "e clientes: seu perfil de interação reforça essa trilha.",
        )

    # ===================== QA ============================================
    @Rule(Resposta(atuacao="testes", entrega="qualidade"))
    def r22_qa_testes_e_qualidade(self):
        self._pontuar(
            "R22", "qa", 8,
            "Testar software e entregar confiabilidade/qualidade é o núcleo de QA.",
        )

    @Rule(Resposta(atuacao="testes", ferramenta=uma_de("python", "javascript")))
    def r23_qa_automacao_de_testes(self):
        self._pontuar(
            "R23", "qa", 4,
            "Testar com Python/JavaScript permite escrever testes automatizados, "
            "diferencial do Engenheiro de Qualidade.",
        )

    # ===================== PRODUTO =======================================
    @Rule(Resposta(atuacao="negocio", social="alto"))
    def r24_pm_negocio_e_pessoas(self):
        self._pontuar(
            "R24", "produto", 8,
            "Decidir o que construir conversando com clientes e times é a ponte "
            "negócio-design-desenvolvimento da Gestão de Produtos.",
        )

    @Rule(Resposta(entrega="valor_negocio", social=uma_de("medio", "alto")))
    def r25_pm_valor_de_negocio(self):
        self._pontuar(
            "R25", "produto", 5,
            "Priorizar o resultado para o negócio, interagindo com pessoas, é típico de "
            "Product Management.",
        )

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
