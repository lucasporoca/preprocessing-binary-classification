# Dados

| Caminho | Conteúdo | Gerado por |
|---|---|---|
| `metadata.csv` | uma linha por base: `dataset_id` (OpenML), instâncias e variáveis antes e depois da limpeza, nº de variáveis numéricas e categóricas, proporção de ausentes, razão de desbalanceamento, tamanho da classe minoritária | `scripts/01_extract_data.py` |
| `01_datasets/<base>.csv` | base processada: colunas `NUM_xx` (numéricas), `CAT_xx` (categóricas) e `target` (0/1) | `scripts/01_extract_data.py` |
| `02_results/<base>_results.csv` | uma linha por algoritmo x pré-processador x perspectiva x partição (2.380 linhas por base), com matriz de confusão, MCC, ROC-AUC, PR-AUC, tempos, memória e tamanho do pipeline | `scripts/02_run_experiments.py` |
| `aggregated_results.csv` | resultados agregados por Dataset x Model x Preprocessor x Perspective | `scripts/03_aggregate_results.py` |
| `03_tests/pvalues/` | matrizes de p-valores ajustados (Wilcoxon pareado + Benjamini-Hochberg) | `scripts/04_statistical_tests.py` |
| `03_tests/ranks/` | rank médio por algoritmo ou pré-processador | `scripts/04_statistical_tests.py` |
| `03_tests/wilcoxon_equality_vs_equity_baseline.csv` | Tabela 1 da monografia: p-valores bruto e ajustado (Igualdade x Equidade no Baseline, por algoritmo) | `scripts/06_perspective_comparison.py` |

Nos arquivos de resultados, `Perspective` é `Equality` (dados puros) ou `Equity` (adequação prévia aos pressupostos do
algoritmo). Os pré-processadores `PCA (Raw)` e `SMOTE (Raw)` (sem padronização prévia) existem nos resultados, mas as
análises usam apenas as versões `PCA (Scaled)` e `SMOTE (Scaled)`, tratadas como `PCA` e `SMOTE`.

## Origem e licenças

Os conjuntos vêm da suíte OpenML-CC18:

> Bischl, B. et al. *OpenML Benchmarking Suites*. 2017. https://arxiv.org/abs/1708.03731
> Vanschoren, J. et al. *OpenML: networked science in machine learning*. SIGKDD Explorations, 15(2), 49-60, 2014.

Cada conjunto pertence aos seus autores originais e mantém a licença e os termos de uso indicados na sua página do
OpenML (`https://www.openml.org/d/<dataset_id>`). A licença MIT deste repositório cobre o código e os resultados
produzidos pelo autor, não os dados de terceiros.
