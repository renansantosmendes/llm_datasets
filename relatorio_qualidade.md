# Relatório de qualidade — synapseai_knowledge_base.jsonl

## Resumo

- Exemplos originais: 736
- Duplicatas exatas removidas: 1
- Exemplos após remoção de duplicatas exatas: 735
- Perguntas com respostas conflitantes (precisam revisão manual): 9
- Respostas sinalizadas como suspeitas: 44
- Exemplos no split de treino final: 677
- Exemplos reservados como teste adversarial: 58
- Exemplos negativos sugeridos (rascunho, requer revisão): 10

## Balanceamento por produto

| Produto | Menções (pergunta + resposta) |
|---|---|
| FinBrain | 127 |
| RiskGen | 124 |
| EduMentor | 121 |
| CourseGen | 107 |
| ClinicaGPT | 105 |

## Balanceamento por setor

| Setor | Menções (pergunta + resposta) |
|---|---|
| Finanças | 4 |
| Educação | 4 |
| Saúde | 4 |

## Perguntas com respostas conflitantes

Estes casos **não foram decididos automaticamente**. Veja o arquivo `conflitos_para_revisar.jsonl` e escolha manualmente a resposta correta (ou escreva uma nova que unifique as informações).

**Quais métricas de observabilidade a SynapseAI monitora?**

- A SynapseAI monitora métricas de qualidade, latência e drift semântico.
- Qualidade das respostas, latência, drift semântico, uso, risco, consistência e cobertura regulatória.

**O que significa isolamento por tenant?**

- Significa que cada cliente (tenant) tem seus dados e recursos completamente isolados dos demais clientes.
- Significa que cada cliente tem seus dados e recursos completamente separados dos demais.

**A SynapseAI faz curadoria de dados?**

- Sim, existe um processo de curadoria de dados nos pipelines de ingestão da empresa.
- Sim, os pipelines incluem processos de curadoria de dados.

**O FinBrain gera relatórios executivos automaticamente?**

- Sim, o FinBrain oferece geração automática de relatórios executivos.
- Sim, o FinBrain oferece geração automática de relatórios executivos em linguagem clara, facilitando a comunicação com diretorias e conselhos.

**O FinBrain reduz o tempo de análise financeira?**

- Sim, este é um dos principais diferenciais de negócio do produto.
- Sim, um dos principais diferenciais do FinBrain é a redução drástica do tempo de análise financeira, transformando processos que levavam horas em minutos.

**O RiskGen substitui equipes jurídicas?**

- Não. O RiskGen não substitui áreas jurídicas ou de compliance, mas reduz o esforço operacional.
- Não. O RiskGen não substitui equipes jurídicas ou de compliance. Seu papel é reduzir esforço operacional, aumentar consistência das análises e minimizar o risco de falhas.

**O EduMentor AI possui app mobile?**

- Sim, disponível em https://app.synapseai.com/edumentor
- Sim, disponível como PWA/Mobile em https://app.synapseai.com/edumentor

**O ClinicaGPT pode acessar diretrizes médicas?**

- Sim, possui RAG sobre diretrizes e protocolos médicos.
- Sim, fornece acesso a protocolos e diretrizes clínicas via consultas em linguagem natural.

**O RiskGen pode monitorar mudanças regulatórias?**

- Utiliza RAG sobre bases documentais versionadas, mas não menciona monitoramento automático de mudanças externas.
- Sim, alerta sobre novas regulações que afetam seus contratos.

## Respostas suspeitas (curtas ou sem pontuação)

- **P:** Qual é o site institucional da SynapseAI Solutions?
  **R:** O site institucional é https://www.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Onde está a documentação geral da SynapseAI?
  **R:** A documentação geral está em https://docs.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é o endereço do console administrativo global da SynapseAI?
  **R:** O console administrativo global está em https://admin.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é o endereço do API Gateway central da SynapseAI?
  **R:** O API Gateway central está em https://api.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL do Web App do FinBrain?
  **R:** https://finbrain.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL base da API do FinBrain?
  **R:** https://api.synapseai.com/finbrain/v1
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Onde está a documentação técnica do FinBrain?
  **R:** https://docs.synapseai.com/finbrain
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL do console administrativo do FinBrain?
  **R:** https://admin.synapseai.com/finbrain
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL do Web App do RiskGen?
  **R:** https://riskgen.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL base da API do RiskGen?
  **R:** https://api.synapseai.com/riskgen/v1
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Onde está a documentação técnica do RiskGen?
  **R:** https://docs.synapseai.com/riskgen
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL do console de auditoria do RiskGen?
  **R:** https://audit.synapseai.com/riskgen
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL do Web App do EduMentor AI?
  **R:** https://edumentor.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** O EduMentor AI possui app mobile?
  **R:** Sim, disponível em https://app.synapseai.com/edumentor
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL base da API do EduMentor AI?
  **R:** https://api.synapseai.com/edumentor/v1
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL do portal institucional do EduMentor AI?
  **R:** https://institutions.synapseai.com/edumentor
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL do editor web do CourseGen Studio?
  **R:** https://coursegen.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL base da API do CourseGen Studio?
  **R:** https://api.synapseai.com/coursegen/v1
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Onde está a documentação técnica do CourseGen Studio?
  **R:** https://docs.synapseai.com/coursegen
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL do Web App do ClinicaGPT?
  **R:** https://clinicagpt.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL base da API do ClinicaGPT?
  **R:** https://api.synapseai.com/clinicagpt/v1
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual é a URL do console hospitalar do ClinicaGPT?
  **R:** https://health.synapseai.com/clinicagpt
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** O EduMentor AI possui app mobile?
  **R:** Sim, disponível como PWA/Mobile em https://app.synapseai.com/edumentor
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual URL para acessar o FinBrain como usuário?
  **R:** https://finbrain.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual URL para desenvolvedores do FinBrain?
  **R:** A API está em https://api.synapseai.com/finbrain/v1 e a documentação em https://docs.synapseai.com/finbrain
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual URL para acessar o RiskGen?
  **R:** https://riskgen.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual URL para auditoria no RiskGen?
  **R:** https://audit.synapseai.com/riskgen
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual URL para instituições no EduMentor AI?
  **R:** https://institutions.synapseai.com/edumentor
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual URL para criar cursos no CourseGen?
  **R:** https://coursegen.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

- **P:** Qual URL para médicos no ClinicaGPT?
  **R:** https://clinicagpt.synapseai.com
  **Motivo:** não termina com pontuação — pode estar truncada ou ser só um token/link

... e mais 14 casos.

## Próximos passos recomendados

1. Abrir `conflitos_para_revisar.jsonl` e decidir, para cada pergunta, qual é a resposta canônica (ou reescrever uma resposta única e completa).
2. Revisar as respostas suspeitas listadas acima e corrigir estilo/pontuação.
3. Revisar `exemplos_negativos_sugeridos.jsonl` — são só um rascunho; confirme que as respostas fazem sentido com o tom da SynapseAI e adicione mais variedade de perguntas fora de domínio.
4. Se algum produto/setor estiver muito abaixo dos demais na tabela de balanceamento, gerar mais exemplos para ele (idealmente com curadoria humana).
5. Usar `synapseai_knowledge_base_limpo.jsonl` para treino e `synapseai_teste_adversarial.jsonl` **somente para avaliação**, nunca para treino.
