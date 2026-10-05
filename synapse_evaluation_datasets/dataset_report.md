# Relatório do dataset de avaliação SynapseAI

Total de itens: **1216**  ·  dev: 206  ·  test: 1010

## Itens por tipo de pergunta × produto

| tipo | FinBrain | RiskGen | EduMentor AI | CourseGen Studio | ClinicaGPT | multi | SynapseAI | none | total |
|---|---|---|---|---|---|---|---|---|---|
| adversarial | 4 | 3 | 2 | 2 | 4 | · | · | 3 | 18 |
| commercial | 31 | 31 | 29 | 29 | 31 | · | · | · | 151 |
| company | 2 | 2 | 2 | 2 | 2 | · | 17 | · | 27 |
| comparison | · | · | · | · | · | 100 | · | · | 100 |
| false_premise | 4 | 4 | 4 | 4 | 4 | · | · | · | 20 |
| lookup | 115 | 119 | 116 | 116 | 117 | · | · | · | 583 |
| multi_column | 11 | 7 | 7 | 7 | 7 | · | · | · | 39 |
| multi_hop | 6 | 6 | 6 | 6 | 6 | · | · | · | 30 |
| out_of_scope | · | · | · | · | · | · | · | 30 | 30 |
| reverse_lookup | 14 | 14 | 17 | 17 | 16 | · | · | · | 78 |
| unanswerable | 14 | 14 | 14 | 14 | 14 | · | · | · | 70 |
| wrong_product | 6 | 6 | 6 | 6 | 6 | · | · | · | 30 |
| yes_no_scope | 8 | 8 | 8 | 8 | 8 | · | · | · | 40 |
| **total** | **215** | **214** | **211** | **211** | **215** | **100** | **17** | **33** | **1216** |

## Dificuldade

- easy: 541
- hard: 148
- medium: 527

## Especificidade (product_specific vs shared_across_products)

- company: 17
- none: 148
- product_specific: 846
- shared_across_products: 205

## Comportamento esperado

- answer: 992
- correct_false_premise: 50
- not_in_docs: 70
- refuse_or_correct: 18
- refuse_out_of_scope: 30
- yes_no: 56

## Modos de avaliação

- rag: 164
- rag+closed_book: 1052

## Tipo de fato

- negative: 148
- stable: 904
- volatile: 164

## Balanço sim/não (itens booleanos)

- sim: 26
- nao: 30

## Comparações (igual vs diferente)

- diferente: 50
- igual: 50

## Contaminação com o dataset de treino informado

- perguntas de treino analisadas: 677
- itens sinalizados `possible_train_leak`: 28
