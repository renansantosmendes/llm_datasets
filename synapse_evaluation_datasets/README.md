# Dataset de avaliação SynapseAI (RAG e fine-tuning)

1.216 itens em português, gerados **sem LLM** a partir das tabelas dos 5 manuais (PDF) e das
propostas/apresentação (PPTX). As respostas de referência são montadas com as próprias células
das tabelas, e o script verifica que cada fato de referência aparece no contexto de origem
(0 itens descartados na validação). Reprodutível: mesma semente, mesmos IDs.

## Arquivos

| Caminho | Para quê |
|---|---|
| `data/synapse_eval_master.jsonl` / `.csv` | Fonte da verdade, com todos os campos |
| `data/subset_closed_book.jsonl` | Itens para modelo **sem** contexto (fine-tuning): estáveis + recusas |
| `data/subset_closed_book_clean.jsonl` | Igual, sem os itens com possível vazamento do treino informado |
| `data/subset_rag_only_volatile.jsonl` | Preços, planos, URLs, headcount: só faz sentido com RAG |
| `frameworks/deepeval_goldens.json` | DeepEval (`Golden`) |
| `frameworks/ragas_samples.jsonl` | RAGAS ≥ 0.2 (`SingleTurnSample`) |
| `frameworks/ragas_legacy.jsonl` | RAGAS ≤ 0.1 (`question`, `ground_truth`) |
| `frameworks/promptfoo/` | `tests.yaml` + `promptfooconfig.yaml` |
| `frameworks/trulens_ground_truth.csv` | TruLens (`query`, `expected_response`) |
| `frameworks/giskard_testset.jsonl` | Giskard 2.x (`QATestset`) |
| `dataset_report.md` | Matrizes de balanceamento |
| `build_eval_dataset.py` | Regenera tudo (`pdftotext`, `python-pptx`, `pyyaml`) |

## Composição

| Tipo | Itens | O que testa |
|---|---|---|
| `lookup` / `reverse_lookup` / `multi_column` | 700 | Consulta a uma linha de tabela, pergunta inversa, várias colunas |
| `commercial` | 151 | Planos e preços das propostas PME e comerciais (**volátil**) |
| `comparison` | 100 | Mesmo tópico em dois produtos (50 "igual", 50 "diferente") |
| `unanswerable` | 70 | Pergunta plausível cuja resposta **não está** na base (ex.: SAP, SOC 2, AWS) |
| `yes_no_scope` | 40 | "O produto faz X?" (20 sim, 20 não) |
| `multi_hop` | 30 | Combina 2 ou 3 tabelas (diagnóstico → estrutura de suporte) |
| `wrong_product` | 30 | Atributo que só existe em **outro** produto |
| `out_of_scope` | 30 | Fora do domínio |
| `company` | 27 | Institucional (missão, pilares, URLs, tecnologia) |
| `false_premise` | 20 | Pede algo que o manual diz que o produto **não** faz |
| `adversarial` | 18 | Injeção de prompt, abuso de escopo, dados de outro tenant |

Os 5 produtos têm entre 211 e 215 itens cada (mais 100 comparações, 17 institucionais e 33 sem produto).
Veja `dataset_report.md` para a matriz completa tipo × produto.

## Campos principais

`question`, `question_variants` (paráfrases para teste de robustez), `reference_answer`,
`key_facts` (fatos que a resposta deve conter), `reference_contexts` (texto de origem),
`sources` (doc, página, seção), `gold_keywords` (âncora para checar se o retriever trouxe o trecho),
`produto`, `question_type`, `difficulty`, `split` (dev 17% / test 83%, por fato),
`eval_modes` (`["rag"]` ou `["rag","closed_book"]`), `expected_behavior`
(`answer`, `yes_no`, `not_in_docs`, `refuse_out_of_scope`, `correct_false_premise`, `refuse_or_correct`),
`volatile`, `specificity`, `possible_train_leak`.

## Como usar

### RAG
Para cada item, rode seu pipeline, guarde a resposta e os **trechos recuperados**, e avalie
fidelidade, recall/precisão de contexto e correção. Use todos os itens (inclusive os voláteis).

```python
from deepeval.dataset import EvaluationDataset
from deepeval.test_case import LLMTestCase

ds = EvaluationDataset()
ds.add_goldens_from_json_file(
    "frameworks/deepeval_goldens.json", input_key_name="input",
    expected_output_key_name="expected_output", context_key_name="context",
    additional_metadata_key_name="additional_metadata")

cases = []
for g in ds.goldens:
    answer, chunks = meu_rag(g.input)              # seu pipeline: texto + lista de trechos
    cases.append(LLMTestCase(input=g.input, actual_output=answer,
                             expected_output=g.expected_output,
                             context=g.context, retrieval_context=chunks))
# evaluate(cases, [FaithfulnessMetric(), ContextualRecallMetric(), ContextualPrecisionMetric(), ...])
```

```python
# RAGAS >= 0.2
import json
from ragas import EvaluationDataset
from ragas.dataset_schema import SingleTurnSample
rows = [json.loads(l) for l in open("frameworks/ragas_samples.jsonl", encoding="utf-8")]
samples = []
for r in rows:
    answer, chunks = meu_rag(r["user_input"])
    samples.append(SingleTurnSample(**r, response=answer, retrieved_contexts=chunks))
ds = EvaluationDataset(samples=samples)
```

### Fine-tuning (closed-book)
Use `data/subset_closed_book_clean.jsonl` (ou os arquivos de `frameworks/`, filtrando
`volatile == False`). Envie **só a pergunta** (com o mesmo system prompt usado no SFT) e compare com
`reference_answer` / `key_facts`. Relatórios que valem a pena:

- **por `produto`**: erro de troca de atributos entre produtos é o risco central do fine-tuning de fatos;
- **por `specificity`**: `product_specific` mede conhecimento; `shared_across_products` (mesma linha em vários manuais) mede muito menos, então reporte separado;
- **por `expected_behavior`**: taxa de recusa correta em `unanswerable`, `out_of_scope`, `wrong_product` e `adversarial`;
- **robustez**: repita com `question_variants`.

### Promptfoo, TruLens, Giskard

```bash
cd frameworks/promptfoo      # edite os providers em promptfooconfig.yaml
promptfoo eval --filter-metadata split=test --filter-metadata volatile=False
```

```python
# Giskard 2.x (o pacote 3.x foi reestruturado e não traz o RAGET): pip install "giskard[llm]<3"
from giskard.rag import QATestset
ts = QATestset.load("frameworks/giskard_testset.jsonl")
```

```python
# TruLens: o CSV tem as colunas query e expected_response
import pandas as pd
gt = pd.read_csv("frameworks/trulens_ground_truth.csv")
# GroundTruthAgreement(gt, provider=...)  (a importação varia conforme a versão do TruLens)
```

## O que foi validado

| Framework | Validação feita |
|---|---|
| DeepEval 4.2 | Carregou os 1.216 goldens e construiu `LLMTestCase` |
| RAGAS 0.4 | Os 1.216 `SingleTurnSample` passaram na validação do schema |
| Promptfoo 0.123 | `validate` OK e `eval` executado (provedor `echo`) com filtro por metadata |
| Giskard | Formato conferido no código da 2.19.2 e carregamento via `pandas.read_json` |
| TruLens | CSV simples; **não executei** o TruLens |

Nenhuma métrica com LLM-juiz foi executada (não há chave de API aqui).

## Limites que você deve conhecer

1. **Cobertura**: as perguntas vêm de **tabelas e slides**. Os parágrafos narrativos dos manuais não geraram
   itens. Para cobri-los, complemente com o pipeline LangChain (`build_synapse_dataset.py`), usando um
   juiz LLM e revisão manual.
2. **Redação das perguntas é por template**: correta, mas menos variada que a de usuários reais. Use
   `question_variants` e considere reescrever uma amostra com um LLM.
3. **Linhas repetidas entre manuais**: 205 itens têm `specificity = shared_across_products`
   (SLAs, rotinas, estrutura de suporte). Eles não distinguem produtos; reporte separado.
4. **Itens voláteis (164)**: preços, planos, URLs e headcount mudam; revise se as propostas forem atualizadas.
5. **Vazamento**: 28 itens se parecem com o `synapseai_knowledge_base_limpo.jsonl` do repositório
   (flag `possible_train_leak`). Rode o gerador com `--train-jsonl seu_sft.jsonl` para checar o **seu** treino.
6. **Atenção ao pipeline de treino**: este dataset vem dos **mesmos documentos**. O
   `build_synapse_dataset.py` retém 15% dos fatos fora do treino por padrão; para medir fine-tuning com
   este dataset, rode-o com `--eval-fraction 0` (o modelo precisa ver os fatos) e mantenha fora do
   treino apenas as **perguntas** deste dataset.
7. A fonte tem um erro de digitação ("profissionals", proposta comercial do ClinicaGPT) que foi mantido
   na referência para ficar fiel ao documento.

## Regenerar

```bash
pip install python-pptx pyyaml            # + pdftotext (poppler-utils)
python build_eval_dataset.py --docs ./synapse_original_documents --out ./synapse_eval \
       --train-jsonl ./seu_sft.jsonl      # opcional: sinaliza vazamento
```
Parâmetros de tamanho: `--per-product-specific`, `--per-product-shared`, `--comparisons-total`,
`--commercial-per-product`, `--unanswerable-per-product`.
