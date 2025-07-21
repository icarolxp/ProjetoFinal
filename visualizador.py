import matplotlib.pyplot as plt
import seaborn as sns
import constantes as const
from matplotlib.patches import Patch
import matplotlib.gridspec as gridspec
import numpy as np


class VisualizadorClimatico:
    """
    Classe responsável por criar diversas visualizações gráficas
    a partir de dados climáticos.
    """
    def __init__(self, dados_para_plotar):
        """
        Inicializa a classe com o DataFrame a ser utilizado nos plots.

        Args:
            dados_para_plotar (pd.DataFrame): DataFrame contendo os dados climáticos.
        """
        self.dados = dados_para_plotar

    def _criar_figura_e_eixo(self, figsize=(10, 6)):
        """
        Cria e retorna uma figura e um eixo do Matplotlib.

        Args:
            figsize (tuple, optional): Tamanho da figura. Padrão é (10, 6).

        Returns:
            tuple: Uma tupla contendo a figura e o eixo (fig, ax).
        """
        fig, ax = plt.subplots(figsize=figsize)
        return fig, ax

    def plotar_graficos(self, style='whitegrid'):
        """
        Plota gráficos de linha para temperatura, umidade e vento, e um gráfico de barras para precipitação.
        """
        sns.set_theme(style=style)
        figures = []
        metricas = [
            (const.COL_TEMP, "Temperatura (°C)", "Temperatura ao Longo do Tempo"),
            (const.COL_UMIDADE, "Umidade (%)", "Umidade ao Longo do Tempo"),
            (const.COL_VENTO, "Velocidade do Vento (km/h)", "Velocidade do Vento ao Longo do Tempo")
        ]

        for metrica, ylabel, title in metricas:
            fig, ax = self._criar_figura_e_eixo()
            sns.lineplot(x=const.COL_DATA, y=metrica, data=self.dados, ax=ax)
            ax.set_title(title)
            ax.set_xlabel("Data")
            ax.set_ylabel(ylabel)
            fig.tight_layout()
            figures.append(fig)

        fig4, ax4 = self._criar_figura_e_eixo(figsize=(12, 6))
        sns.barplot(
            x=const.COL_DATA,
            y=const.COL_PRECIP,
            data=self.dados,
            hue=const.COL_DATA,
            palette="Blues_d",
            legend=False,
            ax=ax4
        )
        ax4.set_title("Precipitação por Dia")
        ax4.set_xlabel("Data")
        ax4.set_ylabel("Precipitação (mm)")
        ax4.tick_params(axis='x', rotation=90)
        fig4.tight_layout()
        figures.append(fig4)

        return figures

    def plotar_estatisticas(self, estatisticas_dict, style='whitegrid'):
        """
        Plota um painel com gráficos de barra para diversas estatísticas resumidas.
        (Versão original com barras simples).
        """
        sns.set_theme(style=style)
        fig, axs = plt.subplots(4, 2, figsize=(12, 18))
        axs = axs.flatten()
        fig.suptitle("Estatísticas Climáticas do Período", fontsize=18, weight='bold')

        cores = sns.color_palette("viridis", len(estatisticas_dict))

        for i, (label, value) in enumerate(estatisticas_dict.items()):
            if i < len(axs):
                ax = axs[i]
                sns.barplot(x=[label], y=[value], hue=[label], ax=ax, palette=[cores[i]], legend=False)
                ax.set_title(label, fontsize=12)
                ax.set_ylabel("Valor")
                ax.set_xticklabels([])
                ax.text(0, value, f'{value:.2f}', ha='center', va='bottom', fontsize=11, weight='bold')
                ax.set_ylim(0, value * 1.2 if value > 0 else 1)

        for i in range(len(estatisticas_dict), len(axs)):
            axs[i].set_visible(False)

        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        return fig

    def plotar_dashboard_hibrido(self, estatisticas_dict):
        """
        Cria um dashboard com 4 cartões de indicadores (KPIs) para as
        principais métricas climáticas do período, incluindo sufixos nas unidades.
        """
        # --- Preparação dos Dados ---
        media_temp = estatisticas_dict.get("Temperatura Média (°C)", 0)
        umidade = estatisticas_dict.get("Umidade Média (%)", 0)
        vento = estatisticas_dict.get("Velocidade Média do Vento (km/h)", 0)
        precipitacao = estatisticas_dict.get("Precipitação Total (mm)", 0)

        # --- Criação do Gráfico ---
        fig = plt.figure(figsize=(10, 8), constrained_layout=True)
        fig.suptitle('Dashboard Climático do Período', fontsize=20, weight='bold')
        gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

        def criar_indicador(ax, titulo, subtitulo, valor, formato, cor_base, sufixo=""):
            """Função auxiliar que agora pode adicionar um sufixo (ex: % ou °C) ao valor."""
            ax.set_facecolor(f'#{cor_base}20')
            ax.text(0.5, 0.75, titulo, ha='center', va='center', fontsize=16, color='#333')
            ax.text(0.5, 0.58, subtitulo, ha='center', va='center', fontsize=10, color='#666')
            
            texto_valor = f"{valor:{formato}}{sufixo}"
            
            ax.text(0.5, 0.25, texto_valor, ha='center', va='center',
                    fontsize=32, fontweight='bold', color=f'#{cor_base}')
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_edgecolor(f'#{cor_base}80')
                spine.set_linewidth(2)

        ax1 = fig.add_subplot(gs[0, 0])
        criar_indicador(ax1, 'Temperatura Média', '(Graus Celsius)', media_temp, '.2f', 'ffb703', sufixo=" °C")

        ax2 = fig.add_subplot(gs[0, 1])
        criar_indicador(ax2, 'Umidade Média', '(Umidade Relativa)', umidade, '.2f', '023e8a', sufixo=" %")

        ax3 = fig.add_subplot(gs[1, 0])
        criar_indicador(ax3, 'Precip. Total', '(Acumulado no período)', precipitacao, ',.2f', '0077b6', sufixo=" mm")

        ax4 = fig.add_subplot(gs[1, 1])
        criar_indicador(ax4, 'Vento Médio', '(Velocidade)', vento, '.2f', '0096c7', sufixo=" km/h")

        return fig

    def plotar_dias_extremos(self, df_extremos, coluna_y, titulo, paleta_cores, unidade):
        """
        Plota os dias com valores extremos (máximos ou mínimos) para uma dada métrica.
        """
        sns.set_theme(style="whitegrid")
        fig, ax = self._criar_figura_e_eixo()

        ascending = "Menores" in titulo
        df_sorted = df_extremos.sort_values(by=coluna_y, ascending=ascending)

        cores = sns.color_palette(paleta_cores, n_colors=len(df_sorted))
        if not ascending:
            cores.reverse()

        sns.barplot(
            x=const.COL_DATA,
            y=coluna_y,
            data=df_sorted,
            hue=const.COL_DATA,
            palette=cores,
            dodge=False,
            ax=ax,
            legend=False
        )

        for i, row in enumerate(df_sorted.itertuples()):
            valor = row[2]
            ax.text(i, valor, f"{valor:.1f}{unidade}", color='black', ha="center", va='bottom', fontweight='bold')

        ax.set_title(titulo, fontsize=16)
        ax.set_xlabel("Data")
        ax.set_ylabel(coluna_y.replace('_', ' ').replace('%', '(%)').capitalize())
        ax.set_xticks(range(len(df_sorted)))
        ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in df_sorted[const.COL_DATA]], rotation=45, ha='right')

        if not df_sorted.empty:
            min_val, max_val = df_sorted[coluna_y].min(), df_sorted[coluna_y].max()
            range_val = max_val - min_val
            if range_val == 0:
                range_val = abs(max_val * 0.2) if max_val != 0 else 1
            ax.set_ylim(min_val - range_val * 0.1, max_val + range_val * 0.1)

        fig.tight_layout()
        return fig

    def plotar_heatmap_correlacao(self, matriz_correlacao, style='whitegrid'):
        """
        Plota um mapa de calor para visualizar a correlação entre variáveis.
        """
        sns.set_theme(style=style)
        fig, ax = self._criar_figura_e_eixo(figsize=(8, 6))
        sns.heatmap(matriz_correlacao, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Mapa de Calor de Correlação entre Variáveis")
        fig.tight_layout()
        return fig


    def plotar_distribuicao(self, coluna, titulo, style='whitegrid'):
        """
        Plota um histograma com títulos e rótulos mais informativos.
        """
        sns.set_theme(style=style)
        fig, ax = self._criar_figura_e_eixo()

        sns.histplot(self.dados[coluna], kde=True, ax=ax, edgecolor='black', alpha=0.7, color='skyblue')

        ax.set_title(f"Histograma das Temperaturas Diárias", fontsize=16)
        ax.set_xlabel(f"{titulo} (°C)", fontsize=12)
        ax.set_ylabel("Número de Dias (Frequência)", fontsize=12)

        ax.tick_params(axis='both', which='major', labelsize=10)
        fig.tight_layout()
        return fig
    def plotar_analise_mensal(self, dados_mensais, style='whitegrid'):
        """
        Plota um gráfico de análise sazonal aprimorado, com rótulos de dados
        e estilo visual refinado.
        """
        sns.set_theme(style=style)
        fig, ax1 = self._criar_figura_e_eixo(figsize=(12, 8))
        fig.suptitle('Análise Mensal: Temperatura vs. Precipitação', fontsize=16, weight='bold')
        
        bar_plot = sns.barplot(
            x=const.COL_DATA,
            y='precipitacao_total',
            data=dados_mensais,
            ax=ax1,
            color='lightblue',
            alpha=0.8,
            edgecolor='black'
        )
        ax1.set_ylabel('Precipitação Acumulada (mm)', color='blue', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.set_xlabel('Mês / Ano', fontsize=12)

        for p in bar_plot.patches:
            ax1.annotate(f'{p.get_height():.1f}',
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center',
                         xytext=(0, 9),
                         textcoords='offset points',
                         fontweight='bold')

        # --- Linha de Temperatura (eixo secundário) ---
        ax2 = ax1.twinx()
        dados_resetados = dados_mensais.reset_index()
        line_plot = ax2.plot(
            dados_resetados.index,
            dados_resetados['temperatura_media'],
            color='red',
            marker='o',
            label='Temperatura Média Mensal'
        )
        ax2.set_ylabel('Temperatura Média (°C)', color='red', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='red')

        for i, txt in enumerate(dados_resetados['temperatura_media']):
            ax2.annotate(f'{txt:.1f}°C', (dados_resetados.index[i], dados_resetados['temperatura_media'][i]),
                         textcoords="offset points",
                         xytext=(0,10),
                         ha='center',
                         fontweight='bold')

        # --- Configurações Finais ---
        ax1.set_xticks(range(len(dados_mensais)))
        ax1.set_xticklabels([d.strftime('%m/%Y') for d in dados_mensais[const.COL_DATA]], rotation=45, ha='right')
        
        # Ocultar a legenda padrão, pois os rótulos já informam tudo
        ax1.get_legend().remove() if ax1.get_legend() else None

        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        return fig
