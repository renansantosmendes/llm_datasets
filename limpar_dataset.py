"""
Script de limpeza e diagnóstico para o dataset synapseai_knowledge_base.jsonl

O que este script faz:
1. Detecta e remove duplicatas exatas (pergunta + resposta idênticas)
2. Detecta perguntas duplicadas com respostas DIFERENTES (conflito) e reporta
   para revisão manual — não decide sozinho qual resposta é a "certa"
3. Detecta respostas muito curtas / estilisticamente fora do padrão
4. Gera um relatório de balanceamento por produto e por setor
5. Separa um conjunto de teste "adversarial" (mantido fora do dataset de treino)
6. Gera um esqueleto de exemplos negativos (fora de domínio) para revisão humana
7. Salva:
   - synapseai_knowledge_base_limpo.jsonl      (pronto para treino)
   - relatorio_qualidade.md                     (relatório legível)
   - conflitos_para_revisar.jsonl               (perguntas duplicadas com respostas diferentes)
   - exemplos_negativos_sugeridos.jsonl         (rascunho, precisa revisão humana)

Uso:
    python limpar_dataset.py caminho/para/synapseai_knowledge_base.jsonl
"""

import json
import sys
import hashlib
import collections
from pathlib import Path

PRODUTOS = ["FinBrain", "RiskGen", "EduMentor", "CourseGen", "ClinicaGPT"]
SETORES = ["Finanças", "Educação", "Saúde"]

# Limite abaixo do qual uma resposta é sinalizada como "curta demais / suspeita"
LIMITE_RESPOSTA_CURTA = 20  # caracteres


def carregar_dataset(caminho):
    exemplos = []
    with open(caminho, encoding="utf-8") as f:
        for i, linha in enumerate(f):
            linha = linha.strip()
            if not linha:
                continue
            try:
                exemplos.append(json.loads(linha))
            except json.JSONDecodeError as e:
                print(f"[AVISO] Linha {i+1} não é um JSON válido e foi ignorada: {e}")
    return exemplos


def extrair_pergunta_resposta(exemplo):
    msgs = exemplo["messages"]
    pergunta = next(m["content"] for m in msgs if m["role"] == "user")
    resposta = next(m["content"] for m in msgs if m["role"] == "assistant")
    system = next((m["content"] for m in msgs if m["role"] == "system"), "")
    return system, pergunta, resposta


def normalizar(texto):
    """Normalização leve só para comparação (não altera o dado original)."""
    return " ".join(texto.strip().lower().split())


def remover_duplicatas_exatas(exemplos):
    """Remove exemplos onde pergunta E resposta são idênticas a outro exemplo já visto."""
    vistos = set()
    unicos = []
    removidos = 0
    for ex in exemplos:
        _, pergunta, resposta = extrair_pergunta_resposta(ex)
        chave = (normalizar(pergunta), normalizar(resposta))
        if chave in vistos:
            removidos += 1
            continue
        vistos.add(chave)
        unicos.append(ex)
    return unicos, removidos


def detectar_conflitos(exemplos):
    """
    Detecta perguntas que aparecem mais de uma vez com respostas DIFERENTES.
    Retorna um dicionário {pergunta_normalizada: [ (exemplo, resposta), ... ]}
    """
    por_pergunta = collections.defaultdict(list)
    for ex in exemplos:
        _, pergunta, resposta = extrair_pergunta_resposta(ex)
        por_pergunta[normalizar(pergunta)].append((ex, resposta))

    conflitos = {}
    for pergunta_norm, ocorrencias in por_pergunta.items():
        respostas_unicas = set(normalizar(r) for _, r in ocorrencias)
        if len(respostas_unicas) > 1:
            conflitos[pergunta_norm] = ocorrencias
    return conflitos


def detectar_respostas_suspeitas(exemplos):
    """Sinaliza respostas muito curtas, sem pontuação final, ou que parecem só uma URL/token solto."""
    suspeitas = []
    for ex in exemplos:
        _, pergunta, resposta = extrair_pergunta_resposta(ex)
        motivo = None
        if len(resposta) < LIMITE_RESPOSTA_CURTA:
            motivo = f"resposta muito curta ({len(resposta)} caracteres)"
        elif not resposta.rstrip().endswith((".", "!", "?", '"')):
            motivo = "não termina com pontuação — pode estar truncada ou ser só um token/link"
        if motivo:
            suspeitas.append({"pergunta": pergunta, "resposta": resposta, "motivo": motivo})
    return suspeitas


def relatorio_balanceamento(exemplos):
    contagem_produtos = {p: 0 for p in PRODUTOS}
    contagem_setores = {s: 0 for s in SETORES}
    for ex in exemplos:
        _, pergunta, resposta = extrair_pergunta_resposta(ex)
        texto = pergunta + " " + resposta
        for p in PRODUTOS:
            if p in texto:
                contagem_produtos[p] += 1
        for s in SETORES:
            if s in texto:
                contagem_setores[s] += 1
    return contagem_produtos, contagem_setores


def separar_conjunto_adversarial(exemplos, fracao=0.08, seed=42):
    """
    Separa uma fatia do dataset como conjunto de teste "adversarial":
    exemplos reservados, nunca usados em treino, para avaliar generalização real.
    Aqui a separação é aleatória; o ideal é depois revisar manualmente e trocar
    por perguntas escritas com fraseado propositalmente diferente do treino.
    """
    import random
    rng = random.Random(seed)
    indices = list(range(len(exemplos)))
    rng.shuffle(indices)
    corte = max(1, int(len(exemplos) * fracao))
    idx_teste = set(indices[:corte])

    treino = [ex for i, ex in enumerate(exemplos) if i not in idx_teste]
    teste = [ex for i, ex in enumerate(exemplos) if i in idx_teste]
    return treino, teste


# Rascunho de exemplos negativos / fora de domínio.
# IMPORTANTE: isto é um ponto de partida. Cada resposta deve ser revisada
# por um humano antes de entrar no dataset de treino de verdade.
PERGUNTAS_FORA_DE_DOMINIO_SUGERIDAS = [
    "Qual é a capital da França?",
    "Vai chover amanhã em São Paulo?",
    "Quem ganhou a última Copa do Mundo?",
    "Qual o resultado de 245 vezes 12?",
    "Quem é o presidente dos Estados Unidos?",
    "Me dá uma receita de bolo de chocolate.",
    "Qual é a cotação do dólar hoje?",
    "Você pode me ajudar com meu currículo?",
    "Qual o melhor filme de 2024?",
    "Como está o trânsito na Avenida Paulista agora?",
]

RESPOSTA_PADRAO_FORA_DE_DOMINIO = (
    "Não tenho informações sobre isso. Posso ajudar com dúvidas sobre os "
    "produtos, tecnologias e serviços da SynapseAI Solutions."
)


def gerar_exemplos_negativos_sugeridos(system_prompt):
    exemplos = []
    for pergunta in PERGUNTAS_FORA_DE_DOMINIO_SUGERIDAS:
        exemplos.append({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pergunta},
                {"role": "assistant", "content": RESPOSTA_PADRAO_FORA_DE_DOMINIO}
            ]
        })
    return exemplos


def salvar_jsonl(exemplos, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        for ex in exemplos:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")


def main():
    if len(sys.argv) < 2:
        print("Uso: python limpar_dataset.py caminho/para/synapseai_knowledge_base.jsonl")
        sys.exit(1)

    caminho_entrada = Path(sys.argv[1])
    pasta_saida = caminho_entrada.parent

    print(f"Carregando {caminho_entrada} ...")
    exemplos = carregar_dataset(caminho_entrada)
    total_original = len(exemplos)
    print(f"Total de exemplos carregados: {total_original}")

    # 1. Duplicatas exatas
    exemplos, n_removidos_exatos = remover_duplicatas_exatas(exemplos)
    print(f"Duplicatas exatas removidas: {n_removidos_exatos}")

    # 2. Conflitos (mesma pergunta, respostas diferentes)
    conflitos = detectar_conflitos(exemplos)
    print(f"Perguntas com respostas conflitantes: {len(conflitos)}")

    # 3. Respostas suspeitas
    suspeitas = detectar_respostas_suspeitas(exemplos)
    print(f"Respostas sinalizadas como suspeitas: {len(suspeitas)}")

    # 4. Balanceamento
    contagem_produtos, contagem_setores = relatorio_balanceamento(exemplos)

    # 5. Split adversarial
    treino, teste_adversarial = separar_conjunto_adversarial(exemplos)
    print(f"Split: {len(treino)} treino / {len(teste_adversarial)} teste adversarial (reservado)")

    # 6. Exemplos negativos sugeridos
    system_prompt = extrair_pergunta_resposta(exemplos[0])[0]
    negativos_sugeridos = gerar_exemplos_negativos_sugeridos(system_prompt)

    # --- Salvando saídas ---
    caminho_limpo = pasta_saida / "synapseai_knowledge_base_limpo.jsonl"
    caminho_teste_adv = pasta_saida / "synapseai_teste_adversarial.jsonl"
    caminho_conflitos = pasta_saida / "conflitos_para_revisar.jsonl"
    caminho_negativos = pasta_saida / "exemplos_negativos_sugeridos.jsonl"
    caminho_relatorio = pasta_saida / "relatorio_qualidade.md"

    salvar_jsonl(treino, caminho_limpo)
    salvar_jsonl(teste_adversarial, caminho_teste_adv)
    salvar_jsonl(negativos_sugeridos, caminho_negativos)

    with open(caminho_conflitos, "w", encoding="utf-8") as f:
        for pergunta_norm, ocorrencias in conflitos.items():
            bloco = {
                "pergunta": ocorrencias[0][1] and next(
                    extrair_pergunta_resposta(ex)[1] for ex, _ in ocorrencias
                ),
                "respostas_conflitantes": [resposta for _, resposta in ocorrencias]
            }
            f.write(json.dumps(bloco, ensure_ascii=False) + "\n")

    # Relatório em markdown
    with open(caminho_relatorio, "w", encoding="utf-8") as f:
        f.write("# Relatório de qualidade — synapseai_knowledge_base.jsonl\n\n")

        f.write("## Resumo\n\n")
        f.write(f"- Exemplos originais: {total_original}\n")
        f.write(f"- Duplicatas exatas removidas: {n_removidos_exatos}\n")
        f.write(f"- Exemplos após remoção de duplicatas exatas: {len(exemplos)}\n")
        f.write(f"- Perguntas com respostas conflitantes (precisam revisão manual): {len(conflitos)}\n")
        f.write(f"- Respostas sinalizadas como suspeitas: {len(suspeitas)}\n")
        f.write(f"- Exemplos no split de treino final: {len(treino)}\n")
        f.write(f"- Exemplos reservados como teste adversarial: {len(teste_adversarial)}\n")
        f.write(f"- Exemplos negativos sugeridos (rascunho, requer revisão): {len(negativos_sugeridos)}\n\n")

        f.write("## Balanceamento por produto\n\n")
        f.write("| Produto | Menções (pergunta + resposta) |\n|---|---|\n")
        for p, c in contagem_produtos.items():
            f.write(f"| {p} | {c} |\n")
        f.write("\n")

        f.write("## Balanceamento por setor\n\n")
        f.write("| Setor | Menções (pergunta + resposta) |\n|---|---|\n")
        for s, c in contagem_setores.items():
            f.write(f"| {s} | {c} |\n")
        f.write("\n")

        f.write("## Perguntas com respostas conflitantes\n\n")
        f.write("Estes casos **não foram decididos automaticamente**. Veja o arquivo "
                 "`conflitos_para_revisar.jsonl` e escolha manualmente a resposta correta "
                 "(ou escreva uma nova que unifique as informações).\n\n")
        for pergunta_norm, ocorrencias in list(conflitos.items())[:20]:
            pergunta_original = next(extrair_pergunta_resposta(ex)[1] for ex, _ in ocorrencias)
            f.write(f"**{pergunta_original}**\n\n")
            for _, resposta in ocorrencias:
                f.write(f"- {resposta}\n")
            f.write("\n")
        if len(conflitos) > 20:
            f.write(f"... e mais {len(conflitos) - 20} casos no arquivo `conflitos_para_revisar.jsonl`.\n\n")

        f.write("## Respostas suspeitas (curtas ou sem pontuação)\n\n")
        for s in suspeitas[:30]:
            f.write(f"- **P:** {s['pergunta']}\n  **R:** {s['resposta']}\n  **Motivo:** {s['motivo']}\n\n")
        if len(suspeitas) > 30:
            f.write(f"... e mais {len(suspeitas) - 30} casos.\n\n")

        f.write("## Próximos passos recomendados\n\n")
        f.write("1. Abrir `conflitos_para_revisar.jsonl` e decidir, para cada pergunta, "
                 "qual é a resposta canônica (ou reescrever uma resposta única e completa).\n")
        f.write("2. Revisar as respostas suspeitas listadas acima e corrigir estilo/pontuação.\n")
        f.write("3. Revisar `exemplos_negativos_sugeridos.jsonl` — são só um rascunho; "
                 "confirme que as respostas fazem sentido com o tom da SynapseAI e adicione mais "
                 "variedade de perguntas fora de domínio.\n")
        f.write("4. Se algum produto/setor estiver muito abaixo dos demais na tabela de "
                 "balanceamento, gerar mais exemplos para ele (idealmente com curadoria humana).\n")
        f.write("5. Usar `synapseai_knowledge_base_limpo.jsonl` para treino e "
                 "`synapseai_teste_adversarial.jsonl` **somente para avaliação**, nunca para treino.\n")

    print("\nArquivos gerados:")
    for caminho in [caminho_limpo, caminho_teste_adv, caminho_conflitos, caminho_negativos, caminho_relatorio]:
        print(f"  - {caminho}")


if __name__ == "__main__":
    main()
