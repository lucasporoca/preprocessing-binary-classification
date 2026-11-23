# Impacto de Técnicas de Pré-processamento no Desempenho de Algoritmos de Classificação Binária

Código-fonte, dados processados e resultados do Trabalho de Conclusão de Curso (Bacharelado em Estatística,
Universidade Federal Fluminense, 2026).

- **Autor:** Lucas Ribeiro Poroca ([ORCID 0009-0009-4894-4848](https://orcid.org/0009-0009-4894-4848)). A monografia foi apresentada sob o nome Lucas de Oliveira Poroca (nome anterior do autor).
- **Orientadora:** Profa. Dra. Karina Yuriko Yaginuma (Departamento de Estatística, UFF)

> **English summary.** Experiment code, processed data and results of an undergraduate thesis that measures how
> 14 data preprocessing techniques (plus a baseline) affect 7 binary classifiers (GNB, LR, KNN, SVM, RF, MLP, XGBoost)
> on the 35 binary datasets of OpenML-CC18. Two perspectives are compared: *Equality* (all algorithms receive the same
> raw data) and *Equity* (each algorithm first receives the adjustments its assumptions require). Performance is measured
> with the Matthews correlation coefficient (MCC) and computational cost, and differences are tested with the paired
> Wilcoxon test with Benjamini-Hochberg correction.

## O que o experimento faz

| Item | Valor |
|---|---|
| Conjuntos de dados | 35 bases binárias da suíte [OpenML-CC18](https://arxiv.org/abs/1708.03731) |
| Algoritmos | GNB, LR, KNN, SVM, RF, MLP, XGBoost (hiperparâmetros padrão) |
| Técnicas de pré-processamento | 14 + baseline (padronização, min-max, IQR capping/remoção, Yeo-Johnson, transformação quantílica, discretização uniforme/quantílica, PCA, LDA, subamostragem aleatória, SMOTE, seleção por ANOVA e por informação mútua) |
| Perspectivas | Igualdade (dados puros para todos) e Equidade (adequação prévia aos pressupostos de cada modelo) |
| Validação | validação cruzada estratificada, 10 partições, semente 42 |
| Métricas | MCC (principal), ROC-AUC, PR-AUC, tempo de treino/predição, pico de memória, tamanho do pipeline em disco |
| Testes | Wilcoxon pareado + correção de Benjamini-Hochberg; diagramas de diferença crítica |

## Estrutura

```
scripts/                  pipeline, executar em ordem numérica
data/
  metadata.csv            características de cada base (instâncias, variáveis, % ausentes, desbalanceamento)
  01_datasets/            bases processadas (saída do script 01)
  02_results/             um CSV de resultados por base, por partição (saída do script 02)
  aggregated_results.csv  resultados agregados (saída do script 03)
  03_tests/               p-valores e ranks dos testes estatísticos (saída do script 05)
images/                   gráficos em PDF (diagramas de diferença crítica, gráficos de bolhas, boxplots)
```

| Script | O que faz | Relação com a monografia |
|---|---|---|
| `01_extract_data.py` | baixa as bases do OpenML e aplica o tratamento inicial | Tabela 2 (Apêndice) |
| `02_run_experiments.py` | executa todos os experimentos (**demora horas**) | base de todos os resultados |
| `03_aggregate_results.py` | agrega as 10 partições por combinação | base de todos os resultados |
| `04_statistical_tests.py` | testes de Wilcoxon + BH e diagramas de diferença crítica | Figuras 9, 10 e 16 a 19 |
| `05_bubble_charts.py` | gráficos de bolhas (custo-benefício) e tabela-resumo | dados-base das Figuras 14, 15, 20 e 21 |
| `06_perspective_comparison.py` | Igualdade x Equidade: teste de Wilcoxon no Baseline e boxplots | Tabela 1 e Figuras 11 a 13 |

Os gráficos têm rótulos em inglês; os da monografia foram traduzidos para o português.

## Como reproduzir

Requer Python 3.10+ (verificado com 3.12) e, para os gráficos, uma instalação LaTeX com o pacote `cm-super`
(exigência do estilo `science` do SciencePlots).

```bash
pip install -r requirements.txt          # ou requirements-lock.txt para as versões exatas verificadas
```

**Opção A, refazer só as análises (minutos).** Os resultados dos experimentos já estão em `data/02_results/`:

```bash
python scripts/03_aggregate_results.py
python scripts/04_statistical_tests.py
python scripts/05_bubble_charts.py
python scripts/06_perspective_comparison.py
```

**Opção B, refazer tudo (horas).** Requer internet para o OpenML. O script 01 apaga e recria `data/01_datasets/`;
o script 02 pula as bases que já têm resultado, então apague `data/02_results/*.csv` para refazer os experimentos:

```bash
python scripts/01_extract_data.py
python scripts/02_run_experiments.py
python scripts/03_aggregate_results.py
# ... demais scripts como na opção A
```

Todas as sementes de aleatoriedade são fixas (42). Colunas de tempo e memória variam conforme a máquina;
as métricas de desempenho dependem das versões das bibliotecas. Em um teste de reexecução na base `kc2`
com as versões de `requirements-lock.txt`, o GNB e o SVM reproduziram os resultados originais, e o MCC médio de
KNN, LR, MLP e RF diferiu em menos de 0,002; o XGBoost diferiu em 0,012. Os arquivos em `data/02_results/` são os
resultados originais da monografia. Os scripts 03 a 06 reproduzem os arquivos em `data/aggregated_results.csv`
e `data/03_tests/` a partir deles.

## Dados

As bases em `data/01_datasets/` são versões tratadas de conjuntos do OpenML-CC18 (colunas constantes removidas,
colunas renomeadas para `NUM_xx` e `CAT_xx`, alvo codificado como `target`). Elas mantêm as licenças e os termos
de uso originais de cada conjunto, consultáveis em `https://www.openml.org/d/<dataset_id>`
(o `dataset_id` está em `data/metadata.csv`). Detalhes em [`data/README.md`](data/README.md).

## Como citar

Use o botão "Cite this repository" do GitHub (arquivo [`CITATION.cff`](CITATION.cff)) ou o DOI do Zenodo
associado a cada versão (release) deste repositório.

## Licença

O código e os resultados produzidos pelo autor estão sob a licença [MIT](LICENSE). Os conjuntos de dados originais
mantêm suas próprias licenças, conforme descrito acima.
