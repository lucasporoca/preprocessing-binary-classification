"""Etapa 6 - Comparação entre as perspectivas Igualdade e Equidade.

1) Tabela 1: teste de Wilcoxon pareado (35 bases) comparando o MCC de Igualdade
   e Equidade no cenário Baseline, para cada algoritmo, com correção de
   Benjamini-Hochberg sobre os 7 algoritmos.
2) Figura 11: boxplot do MCC por algoritmo, Igualdade x Equidade, no Baseline.
3) Figuras 12 e 13: boxplots do impacto no MCC (delta = MCC da técnica - MCC do
   baseline da mesma perspectiva, por base) para cada algoritmo e técnica.

Entrada : data/aggregated_results.csv
Saída   : data/03_tests/wilcoxon_equality_vs_equity_baseline.csv
          images/boxplots/*.pdf
Uso     : python scripts/06_perspective_comparison.py   (requer LaTeX para o estilo "science")
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests

plt.style.use(['science'])

BASE_DIR = Path(__file__).resolve().parent.parent
IMG_DIR = BASE_DIR / "images/boxplots"
TEST_DIR = BASE_DIR / "data/03_tests"
IMG_DIR.mkdir(parents=True, exist_ok=True)
TEST_DIR.mkdir(parents=True, exist_ok=True)

METRIC = "Test_MCC"
MODELS = ['GNB', 'LR', 'KNN', 'SVM', 'RF', 'MLP', 'XGB']
PREPROCESSORS = [
    'Standard Scaling', 'MinMax Scaling', 'IQR Capping', 'IQR Removal', 'Yeo-Johnson',
    'Quantile Transform', 'Uniform Binning', 'Quantile Binning', 'PCA', 'LDA',
    'Random Undersampling', 'SMOTE', 'Select Percentile (ANOVA)', 'Select Percentile (MI)',
]
COLORS = {'Equality': '#4C72B0', 'Equity': '#55A868'}


def load_data():
    df = pd.read_csv(BASE_DIR / 'data/aggregated_results.csv')
    df = df[~df['Preprocessor'].str.contains(r'PCA \(Raw\)|SMOTE \(Raw\)', regex=True, na=False)].copy()
    df['Preprocessor'] = df['Preprocessor'].replace({'PCA (Scaled)': 'PCA', 'SMOTE (Scaled)': 'SMOTE'})
    return df


def wilcoxon_equality_vs_equity(df):
    base = df[df['Preprocessor'] == 'Baseline']
    raw_p = []
    for model in MODELS:
        wide = base[base['Model'] == model].pivot(index='Dataset', columns='Perspective', values=METRIC)
        if np.allclose(wide['Equality'], wide['Equity']):
            raw_p.append(1.0)
        else:
            raw_p.append(wilcoxon(wide['Equality'], wide['Equity'], zero_method='pratt').pvalue)
    adj_p = multipletests(raw_p, alpha=0.05, method='fdr_bh')[1]
    table = pd.DataFrame({
        'Model': MODELS,
        'p_value_raw': raw_p,
        'p_value_adjusted': adj_p,
        'Significant': adj_p < 0.05,
    })
    table.to_csv(TEST_DIR / 'wilcoxon_equality_vs_equity_baseline.csv', index=False)
    return table


def plot_baseline_boxplot(df):
    base = df[df['Preprocessor'] == 'Baseline']
    fig, ax = plt.subplots(figsize=(7.1, 3.0))
    sns.boxplot(data=base, x='Model', y=METRIC, hue='Perspective', order=MODELS,
                hue_order=['Equality', 'Equity'], palette=COLORS, linewidth=0.8,
                fliersize=2, ax=ax)
    ax.set_xlabel('Algorithm')
    ax.set_ylabel('MCC')
    ax.legend(title=None, frameon=False)
    fig.savefig(IMG_DIR / 'boxplot_baseline_equality_vs_equity.pdf', format='pdf',
                transparent=True, bbox_inches='tight')
    plt.close(fig)


def compute_delta(df):
    base = df[df['Preprocessor'] == 'Baseline'][['Dataset', 'Model', 'Perspective', METRIC]]
    base = base.rename(columns={METRIC: 'Baseline_MCC'})
    out = df[df['Preprocessor'] != 'Baseline'].merge(base, on=['Dataset', 'Model', 'Perspective'])
    out['Delta_MCC'] = out[METRIC] - out['Baseline_MCC']
    return out


def plot_delta_boxplots(delta, models, filename):
    fig, axes = plt.subplots(len(models), 2, figsize=(7.1, 3.3 * len(models)))
    for row, model in enumerate(models):
        sub = delta[delta['Model'] == model]
        for col, persp in enumerate(['Equality', 'Equity']):
            ax = axes[row, col]
            data = sub[sub['Perspective'] == persp]
            sns.boxplot(data=data, x='Delta_MCC', y='Preprocessor', order=PREPROCESSORS,
                        color=COLORS[persp], linewidth=0.7, fliersize=1.5, ax=ax)
            ax.axvline(0, color='black', linestyle='--', linewidth=0.6, zorder=0)
            ax.set_title(persp if row else f'{model}\n{persp}', fontsize=8)
            ax.set_xlabel(r'$\Delta$ MCC')
            ax.set_ylabel('')
            ax.tick_params(axis='y', labelsize=6)
            if col == 1:
                ax.set_yticklabels([])
        axes[row, 0].set_ylabel(model, fontsize=9)
    fig.tight_layout()
    fig.savefig(IMG_DIR / filename, format='pdf', transparent=True, bbox_inches='tight')
    plt.close(fig)


def main():
    df = load_data()
    wilcoxon_equality_vs_equity(df)
    plot_baseline_boxplot(df)
    delta = compute_delta(df)
    plot_delta_boxplots(delta, ['GNB', 'LR', 'KNN', 'SVM'], 'boxplot_delta_mcc_part1.pdf')
    plot_delta_boxplots(delta, ['RF', 'MLP', 'XGB'], 'boxplot_delta_mcc_part2.pdf')


if __name__ == "__main__":
    main()
