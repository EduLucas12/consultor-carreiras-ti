"""As 10 trilhas de carreira do escopo do trabalho (a "saída" do sistema)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Trilha:
    id: str
    nome: str
    foco: str
    comecar_por: tuple[str, ...]


# A ORDEM aqui é a ordem de desempate (ver motor.py) e a ordem dos gráficos.
TRILHAS: dict[str, Trilha] = {
    t.id: t
    for t in (
        Trilha(
            "backend",
            "Desenvolvimento Back-end",
            "Lógica de servidores, construção de APIs, regras de negócio e bancos de dados.",
            (
                "Domine uma linguagem de servidor (Python, Java, C#, Node.js...).",
                "Construa uma API REST com banco de dados relacional.",
                "Estude modelagem de dados, SQL e autenticação.",
            ),
        ),
        Trilha(
            "frontend",
            "Desenvolvimento Front-end & UI/UX",
            "Interfaces web responsivas, experiência do usuário e frameworks reativos.",
            (
                "HTML, CSS e JavaScript sólidos antes de qualquer framework.",
                "Um framework reativo (React, Vue, Angular...).",
                "Acessibilidade, responsividade e noções de design/UX.",
            ),
        ),
        Trilha(
            "ciencia_dados",
            "Ciência de Dados e Machine Learning",
            "Estatística, modelagem preditiva, análise de grandes massas de dados e IA.",
            (
                "Estatística e probabilidade (a base de tudo).",
                "Python com pandas e scikit-learn.",
                "Projetos de previsão com avaliação honesta de modelos.",
            ),
        ),
        Trilha(
            "engenharia_dados",
            "Engenharia de Dados",
            "Arquitetura de dados, pipelines (ETL/ELT) e infraestrutura para Data Lakes.",
            (
                "SQL avançado e modelagem de dados.",
                "Conceitos de ETL/ELT e orquestração de pipelines.",
                "Data warehouse / data lake e processamento em lote e streaming.",
            ),
        ),
        Trilha(
            "ciberseguranca",
            "Cibersegurança (Security / Pentesting)",
            "Defesa cibernética, análise de vulnerabilidades, criptografia e redes seguras.",
            (
                "Redes (TCP/IP) e Linux.",
                "Vulnerabilidades web (OWASP Top 10) e criptografia básica.",
                "Prática em laboratórios e desafios CTF.",
            ),
        ),
        Trilha(
            "devops",
            "DevOps & SRE",
            "Automação de processos, integração e entrega contínua (CI/CD) e contêineres.",
            (
                "Linux, Git e scripts de automação.",
                "Pipelines de CI/CD e contêineres (Docker).",
                "Monitoramento, logs e confiabilidade (SRE).",
            ),
        ),
        Trilha(
            "cloud",
            "Computação em Nuvem (Cloud Architecture)",
            "Planejamento, migração e gestão de infraestruturas escaláveis (AWS/Azure/GCP).",
            (
                "Fundamentos de nuvem em um provedor (AWS, Azure ou GCP).",
                "Redes, armazenamento, custos e escalabilidade.",
                "Infraestrutura como código e arquitetura de referência.",
            ),
        ),
        Trilha(
            "mobile",
            "Desenvolvimento Mobile",
            "Ecossistema de dispositivos móveis (nativo ou multiplataforma com Flutter/React Native).",
            (
                "Escolha um caminho: Flutter/Dart, React Native ou nativo (Kotlin/Swift).",
                "Publique um app simples ponta a ponta.",
                "Ciclo de vida do app, navegação, consumo de APIs e armazenamento local.",
            ),
        ),
        Trilha(
            "qa",
            "Engenharia de Qualidade e Testes (QA)",
            "Testes automatizados, confiabilidade de software e processos de qualidade.",
            (
                "Fundamentos de teste de software (tipos, técnicas, casos de teste).",
                "Automação de testes (pytest, Selenium/Playwright) e testes de API.",
                "Integração dos testes ao CI/CD e métricas de qualidade.",
            ),
        ),
        Trilha(
            "produto",
            "Gestão de Produtos (Product Management)",
            "Ponte entre negócio, design e desenvolvimento, metodologias ágeis e priorização.",
            (
                "Metodologias ágeis (Scrum/Kanban) e discovery de produto.",
                "Priorização, roadmap e métricas de produto.",
                "Comunicação com clientes, design e engenharia.",
            ),
        ),
    )
}
