import numpy as np
import matplotlib.ticker as tkr
import matplotlib.pyplot as plt
from matplotlib import cm

# VALORES CHAVE

rendimento_relevante_irs = 0.75 # os TI tributam sobre 75% do Rendimento Global
rendimento_relevante_ss = 0.70 # os TI pagam Segurança Social sobre 70% do Rendimento Global
minimo_existencia = 9215.00
taxa_ss_ti = 0.214 # os TI pagam 21.4% de Segurança Social
deducoes_a_colecta = 604.52 # Pré-calculado, explicado na nota
beneficio_municipal = 0.025 # No caso de Lisboa, 2.5% da colecta liquida
deducao_especifica = 4104

escaloes_irs_2022 = [
    [7112.00, 0.145],
    [10732.00, 0.23],
    [15216.00, 0.265],
    [19696.00, 0.285],
    [25067.00, 0.35],
    [36757.00, 0.37],
    [53042.00, 0.435],
    [75000.00, 0.46],
    [None, 0.48]
]

escaloes_irs_2021 = [
    [7112.00, 0.145],
    [10732.00, 0.23],
    [20322.00, 0.285],
    [25075.00, 0.35],
    [36967.00, 0.37],
    [80640.00, 0.45],
    [None, 0.48]
]

# CONFIGURAÇÃO DA SIMULAÇÃO

# Simular para rendimentos no intervalo
inicio_rendimentos = 5000
# até
final_rendimentos = 150000
# em intervalos de
intervalo = 50


# PROGRAMA

def colecta_liquida(colecta):
    colecta = max(0,colecta-deducoes_a_colecta)
    return colecta-colecta*beneficio_municipal

def calc_colecta(glob_rend, escaloes, independente):
    if glob_rend < minimo_existencia:
        colecta = 0.0
    else:
        if independente:
            rend_tributavel = glob_rend*rendimento_relevante_irs
        else:
            rend_tributavel = glob_rend-deducao_especifica
        i = len(escaloes)
        colecta = 0
        while i>0:
            i -= 1
            patamar = 0.0
            if i>0: patamar = escaloes[i-1][0]
            porcao = max(0,rend_tributavel-patamar)
            if porcao>0:
                colecta += porcao*escaloes[i][1]
                rend_tributavel -= porcao
    return colecta

def simular(titulo, independente):
    rendimentos = np.arange(inicio_rendimentos,final_rendimentos+intervalo,intervalo)
    dados = []
    for rendimento in rendimentos:
        irs_2021 = calc_colecta(rendimento, escaloes_irs_2021, independente)
        irs_2022 = calc_colecta(rendimento, escaloes_irs_2022, independente)
        diff = irs_2021-irs_2022
        percentagem_21 = irs_2021/rendimento
        percentagem_22 = irs_2022/rendimento
        irs_21_liquido = colecta_liquida(irs_2021)
        irs_22_liquido = colecta_liquida(irs_2022)
        diff_liquido = irs_21_liquido-irs_22_liquido
        percentagem_22_liquida = irs_22_liquido/rendimento
        dados.append([rendimento, irs_2021, irs_2022, diff, percentagem_21, percentagem_22, irs_22_liquido, percentagem_22_liquida, diff_liquido])

    cor_colecta = 'dodgerblue'
    cor_percentagem = 'forestgreen'
    cor_diferenca = 'tomato'
    cor_grelha_colecta_percentagem = 'teal'

    
    fig, ax = plt.subplots(1, 1, figsize=(15,8))
    fig.subplots_adjust(left=0.15, bottom=0.15)

    ax2 = ax.twinx()
    ax3 = ax.twinx()
    ax2.yaxis.set_label_position('left')
    ax2.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(("axes", -0.1))
    ax2.spines['left'].set_position(("axes", 0))
    dados = np.array(dados)
    ax.plot(dados[:,0], dados[:,1], label="Colecta IRS 2021", color=cor_colecta, linewidth=1, linestyle='--')
    ax.plot(dados[:,0], dados[:,2], label="Colecta IRS 2022", color=cor_colecta, linewidth=1, linestyle='-')
    ax.plot(dados[:,0], dados[:,6], label="Colecta Liquida* 2022", color=cor_colecta, linewidth=3, linestyle='-')
    ax2.plot(dados[:,0], 100*dados[:,4], label="Percentagem 2021", color=cor_percentagem, linewidth=1, linestyle='--')
    ax2.plot(dados[:,0], 100*dados[:,5], label="Percentagem 2022", color=cor_percentagem, linewidth=1, linestyle='-')
    ax2.plot(dados[:,0], 100*dados[:,7], label="Percentagem 2022 Liquida*", color=cor_percentagem, linewidth=3, linestyle='-')
    ax3.plot(dados[:,0], dados[:,3], label="Differença", color=cor_diferenca, linewidth=1, linestyle='-')
    ax3.plot(dados[:,0], dados[:,8], label="Differença Liquida*", color=cor_diferenca, linewidth=3, linestyle='-')

    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"

    x_tick_positions = np.arange(min(ax.get_xticks()),max(ax.get_xticks()),2500)
    ax.set_xticks(x_tick_positions);
    ax.set_xticklabels(x_tick_positions, rotation=70);
    ax.set_yticks(np.arange(min(ax.get_yticks()),max(ax.get_yticks()),2000));
    ax.set_yticklabels(ax.get_yticks(), fontweight='bold');
    ax2.set_yticklabels(ax2.get_yticks(), fontweight='bold');
    ax3.set_yticklabels(ax3.get_yticks(), fontweight='bold');
    #ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.0f} €'.format))
    ax.xaxis.set_major_formatter(tkr.FuncFormatter(lambda x, p: format(int(x), ',') + " €"))

    ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.0f} €'.format))
    ax2.yaxis.set_major_formatter(plt.FuncFormatter('{:.2f}%'.format))
    ax3.yaxis.set_major_formatter(plt.FuncFormatter('{:.2f} €'.format))
    ax.yaxis.label.set_color(cor_colecta)
    ax2.yaxis.label.set_color(cor_percentagem)
    ax3.yaxis.label.set_color(cor_diferenca)
    ax.tick_params(colors=cor_colecta, axis='y')
    ax2.tick_params(colors=cor_percentagem, axis='y')
    ax3.tick_params(colors=cor_diferenca, axis='y')

    ax.set_xlim(inicio_rendimentos, final_rendimentos)
    ax2.set_xlim(inicio_rendimentos, final_rendimentos)
    ax3.set_xlim(inicio_rendimentos, final_rendimentos)
    ax.set_ylim(0, ax.get_ylim()[1])
    ax2.set_ylim(0, ax2.get_ylim()[1])

    plt.suptitle(titulo, fontsize=14)
    ax.set_xlabel("Rendimento Global Bruto", fontweight='bold')
    ax.set_ylabel("Colecta IRS", fontweight='bold')
    ax2.set_ylabel("Colecta como Percentagem do rendimento", fontweight='bold')
    ax3.set_ylabel("Poupança de 2021 para 2022", fontweight='bold')



    ax.grid(color=cor_grelha_colecta_percentagem, alpha=0.3)
    ax3.grid(axis='y', color=cor_diferenca, linestyle='--', linewidth=1, alpha=0.5)

    lines_labels = [a.get_legend_handles_labels() for a in fig.axes]
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    fig.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.4, 0.95), ncol=4)
    nota = """* Para o cálculo da colecta líquida, 
    considerou-se um total de deduções à colecta de 604.52€,
    mais 2.5% de Benefício Municial (e.g. Lisboa).
    As deduções correspondem a 50€ em Saúde, renda de 800€, 
    50€ de IVA de facturas, 20€ de Passes, e 250€ de despesas gerais.
    """
    plt.figtext(0.85, 0.90, nota, wrap=True, horizontalalignment='center', fontsize=8)
    #plt.tight_layout()
    fig.show()
    

simular("Colecta de IRS Trabalhadores Independentes 2021 vs 2022", True)
simular("Colecta de IRS Trabalhadores Dependentes 2021 vs 2022", False)

plt.show()