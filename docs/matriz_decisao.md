# Matriz de Decisão (Fase 1 – Engenharia de Conhecimento)

Esta tabela mostra **como as respostas do usuário ativam as regras de cada trilha**.
Cada regra cruza 2 ou 3 respostas (por isso evita ambiguidades) e soma ou subtrai pontos.
A trilha com mais pontos vence (regra `decisao_final`).

> Os pesos (+8, +5, +3…) são **julgamento do autor**, não verdade científica: refletem
> o quanto cada combinação é *característica* da trilha (+8 = combinação que define a trilha;
> +2/+3 = indício de apoio; negativo = fator contrário). Em um sistema real, seriam calibrados
> com especialistas humanos (Aquisição de Conhecimento, Aula 8).

## 1. Vocabulário (as perguntas e valores possíveis)

| Pergunta (slot do fato `Resposta`) | Valores |
|---|---|
| `matematica` | baixa · media · alta |
| `atuacao` | algoritmos · layouts · servidores · dados_brutos · seguranca · automacao · testes · negocio |
| `ferramenta` | python · javascript · sql · linux_redes · mobile_lang · nenhuma |
| `entrega` | produto_final · infraestrutura · seguranca · insights · qualidade · valor_negocio |
| `foco_dados` *(extra)* | modelos · pipelines · nenhum |
| `foco_infra` *(extra)* | nuvem · ci_cd · nenhum |
| `plataforma` *(extra)* | web · celular · indiferente |
| `social` *(extra)* | baixo · medio · alto |

As quatro últimas perguntas foram acrescentadas porque as 4 dimensões do enunciado não
separam 10 trilhas (ex.: sem `foco_dados`, Ciência e Engenharia de Dados ficam idênticas).

## 2. Regras (SE condições ENTÃO pontos para a trilha)

| ID | Trilha | SE (todas as condições) | Pontos |
|---|---|---|---:|
| R01 | Back-end | atuacao=algoritmos **E** ferramenta∈{python, sql, javascript, mobile_lang} **E** foco_dados=nenhum **E** plataforma∈{web, indiferente} | +6 |
| R02 | Back-end | atuacao=algoritmos **E** entrega∈{produto_final, infraestrutura} **E** foco_dados=nenhum **E** plataforma∈{web, indiferente} | +4 |
| R03 | Front-end | atuacao=layouts **E** ferramenta=javascript | +7 |
| R04 | Front-end | atuacao=layouts **E** entrega=produto_final **E** plataforma=web | +5 |
| R05 | Front-end | atuacao=layouts **E** plataforma=celular *(penalidade de desambiguação)* | −2 |
| R06 | Mobile | plataforma=celular **E** atuacao∈{layouts, algoritmos} | +5 |
| R07 | Mobile | plataforma=celular **E** ferramenta∈{mobile_lang, javascript} **E** entrega=produto_final | +5 |
| R08 | Ciência de Dados | matematica=alta **E** atuacao=dados_brutos **E** foco_dados=modelos | +8 |
| R09 | Ciência de Dados | entrega=insights **E** foco_dados=modelos **E** ferramenta∈{python, sql} | +5 |
| R10 | Ciência de Dados | matematica=baixa **E** foco_dados=modelos *(penalidade: falta base estatística)* | −4 |
| R11 | Engenharia de Dados | atuacao=dados_brutos **E** foco_dados=pipelines **E** ferramenta∈{python, sql} | +8 |
| R12 | Engenharia de Dados | foco_dados=pipelines **E** entrega=infraestrutura | +5 |
| R13 | Engenharia de Dados | matematica∈{baixa, media} **E** atuacao=dados_brutos **E** foco_dados=pipelines | +2 |
| R14 | Cibersegurança | atuacao=seguranca **E** entrega=seguranca | +8 |
| R15 | Cibersegurança | atuacao=seguranca **E** ferramenta=linux_redes | +5 |
| R16 | DevOps & SRE | atuacao=automacao **E** foco_infra=ci_cd | +8 |
| R17 | DevOps & SRE | ferramenta=linux_redes **E** foco_infra=ci_cd **E** entrega=infraestrutura | +5 |
| R18 | DevOps & SRE | atuacao=servidores **E** foco_infra=ci_cd | +3 |
| R19 | Cloud | foco_infra=nuvem **E** entrega=infraestrutura | +7 |
| R20 | Cloud | atuacao=servidores **E** foco_infra=nuvem | +5 |
| R21 | Cloud | atuacao∈{servidores, automacao} **E** foco_infra=nuvem **E** social∈{medio, alto} | +3 |
| R22 | QA | atuacao=testes **E** entrega=qualidade | +8 |
| R23 | QA | atuacao=testes **E** ferramenta∈{python, javascript} | +4 |
| R24 | Gestão de Produtos | atuacao=negocio **E** social=alto | +8 |
| R25 | Gestão de Produtos | entrega=valor_negocio **E** social∈{medio, alto} | +5 |

Mais a regra **`decisao_final`** (salience −100, roda por último): escolhe a trilha de maior
pontuação, calcula a confiança e monta o resultado.

## 3. Regras de desambiguação (os pares que o enunciado pede para separar)

| Par confundível | O que separa | Regras |
|---|---|---|
| Cientista × Engenheiro de Dados | `foco_dados` (modelos × pipelines) e a matemática (alta favorece Ciência; baixa a penaliza) | R08, R09, R10 × R11, R12, R13 |
| DevOps × Cloud | `foco_infra` (ci_cd × nuvem) | R16–R18 × R19–R21 |
| Front-end × Mobile | `plataforma` (web × celular) | R04, R05 × R06, R07 |
| Back-end × Dados | `foco_dados` precisa ser "nenhum" para o Back-end pontuar | R01, R02 |

## 4. Critério de decisão

- Vence a trilha com mais pontos. Empate no topo é sinalizado (`empate`) e a confiança cai para "baixa".
- **Inconclusivo**: se a melhor trilha tiver menos de 5 pontos, o sistema admite que não sabe.
- **Confiança**: margem entre 1ª e 2ª ≥ 5 → alta · ≥ 2 → média · senão → baixa.

## 5. Mapa trilha × perguntas (onde cada trilha "se ancora")

| Trilha | Respostas-âncora (as que mais pesam) |
|---|---|
| Back-end | atuacao=algoritmos, foco_dados=nenhum |
| Front-end | atuacao=layouts, ferramenta=javascript, plataforma=web |
| Mobile | plataforma=celular |
| Ciência de Dados | matematica=alta, foco_dados=modelos, entrega=insights |
| Engenharia de Dados | foco_dados=pipelines, atuacao=dados_brutos |
| Cibersegurança | atuacao=seguranca, entrega=seguranca |
| DevOps & SRE | atuacao=automacao, foco_infra=ci_cd |
| Cloud | foco_infra=nuvem, entrega=infraestrutura |
| QA | atuacao=testes, entrega=qualidade |
| Gestão de Produtos | atuacao=negocio, social=alto, entrega=valor_negocio |
