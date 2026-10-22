# 🧭 Consultor Inteligente de Carreiras em TI

Sistema Especialista baseado em regras (Python + [Experta](https://github.com/nilp0inter/experta) + Streamlit)
que entrevista o usuário e recomenda **uma entre 10 trilhas de carreira em TI**, justificando a decisão
com as regras que dispararam.

**Disciplina:** Inteligência Artificial · **Curso:** Ciência da Computação · **UNIPAC Barbacena**
**Professor:** Felipe Roncalli de Paula Carneiro · **Aluno(a):** Lucas Eduardo Silva

## As 10 trilhas

Back-end · Front-end & UI/UX · Ciência de Dados e ML · Engenharia de Dados · Cibersegurança ·
DevOps & SRE · Computação em Nuvem · Mobile · Engenharia de Qualidade (QA) · Gestão de Produtos

## Requisitos

- Python **3.10 ou superior**
- Git (para clonar/publicar)

## Instalação

```bash
# 1) (recomendado) ambiente virtual
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2) dependências  — são DUAS etapas, de propósito (veja a nota abaixo)
pip install -r requirements.txt
pip install --no-deps experta
```

> **Por que duas etapas?** O Experta declara `frozendict==1.2`, uma versão antiga que não compila
> em Pythons recentes. Instalamos o `frozendict` atual e o Experta com `--no-deps`.
> Além disso, o Experta usa `collections.Mapping` (removido no Python 3.10); o arquivo
> `consultor/compat.py` corrige isso e **deve ser importado antes do `experta`**.

## Executar

```bash
streamlit run app.py
```

Abra o endereço mostrado no terminal (normalmente http://localhost:8501).
Na barra lateral há o **modo demonstração**: carregue uma persona de teste e clique em
"Descobrir minha trilha".

## Testes (validação com personas)

```bash
pytest -q
```

São 32 testes: 11 personas (cobrindo as 10 trilhas, incluindo as 4 exigidas), pares confundíveis
(Ciência × Engenharia de Dados, DevOps × Cloud, Front-end × Mobile), regras mortas, consistência
da documentação e a própria interface (via `streamlit.testing.v1.AppTest`).

Ferramentas extras de engenharia de conhecimento:

```bash
python scripts/cobertura.py 4000      # quem vence, quantos inconclusivos, regras que nunca disparam
python scripts/depurar.py "Bruno"     # mostra a ordem em que o Experta dispara as regras
```

## Como funciona

| Componente (Aula 8)        | Onde está                                                     |
|----------------------------|---------------------------------------------------------------|
| Base de Conhecimento       | 25 regras `@Rule` em `consultor/motor.py` (R01–R25)           |
| Motor de Inferência        | Experta, encadeamento para frente (*forward chaining*)        |
| Memória de Trabalho        | fato `Resposta` + pontuação acumulada                         |
| Interface com o Usuário    | `app.py` (Streamlit)                                          |
| Explicador                 | lista de `Disparo` (regra, pontos, motivo) exibida na tela    |
| Aquisição de Conhecimento  | `docs/matriz_decisao.md` (a tabela de decisão)                |

Fluxo: respostas → fato `Resposta` → cada regra cruza 2–3 respostas e soma/subtrai pontos de uma
trilha (registrando o motivo) → a regra `decisao_final` (por último, `salience=-100`) escolhe a
vencedora, calcula a confiança e entrega a justificativa. Se nenhuma trilha atinge 5 pontos, o
sistema responde **"inconclusivo"** em vez de chutar.

## Estrutura

```
app.py                     interface Streamlit
consultor/
  compat.py                remendo do Experta p/ Python >= 3.10
  perguntas.py             vocabulário: perguntas e valores válidos
  trilhas.py               as 10 trilhas (+ "por onde começar")
  motor.py                 fatos, 25 regras, regra de decisão, recomendar()
  personas.py              personas de teste
tests/                     pytest (motor, personas, interface)
scripts/                   cobertura.py, depurar.py
docs/
  matriz_decisao.md        Fase 1: matriz de decisão
```

## Publicar no GitHub

```bash
git init
git add .
git commit -m "Consultor de Carreiras em TI - sistema especialista"
git branch -M main
git remote add origin https://github.com/<seu-usuario>/<seu-repo>.git
git push -u origin main
```

## Sobre o histórico de commits

O histórico deste repositório foi organizado em commits temáticos a partir de uma versão do projeto
já desenvolvida, e por isso todos os commits têm a mesma data (21/10/2026). As datas **não**
representam o ritmo real de desenvolvimento; os commits servem para separar, por assunto, as etapas
do trabalho (engenharia de conhecimento, motor, regras, testes e interface).

## Limitações (honestas)

- Os **pesos** das regras são julgamento do autor, não dados empíricos: refletem o conhecimento de
  um "especialista" e precisariam de calibração com profissionais reais (gargalo da aquisição de conhecimento).
- O sistema é **rígido**: só conhece as 8 perguntas e as 10 trilhas; respostas incoerentes ou perfis
  mistos tendem ao resultado inconclusivo.
- Recomendação é apoio à reflexão, não orientação profissional.
