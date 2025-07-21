import pandas as pd
import numpy as np
from estacao import EstacaoMeteorologica
import constantes as const


def _filtrar_por_data_inicio(df, data_inicio):
    """Função auxiliar para filtrar um DataFrame a partir de uma data de início."""
    if data_inicio is None:
        return df
    return df[df[const.COL_DATA] >= data_inicio]


def _filtrar_por_data_fim(df, data_fim):
    """Função auxiliar para filtrar um DataFrame até uma data de fim."""
    if data_fim is None:
        return df
    return df[df[const.COL_DATA] <= data_fim]


class AnalisadorClimatico:
    """
    Realiza análises complexas sobre os dados de uma EstacaoMeteorologica,
    incluindo estatísticas, filtragem e geração de resumos.
    """
    def __init__(self, caminho_csv):
        """
        Inicializa o analisador.

        Args:
            caminho_csv (str): O caminho para o arquivo CSV com os dados.
        """
        self.estacao = EstacaoMeteorologica(caminho_csv)
        self.dados_completos = self.estacao.get_dados()
        self.caminho_csv = caminho_csv

    def get_dados_completos(self):
        """Retorna o DataFrame completo sem filtros."""
        return self.dados_completos

    def get_dados_filtrados_para_plot(self, data_inicio=None, data_fim=None):
        """
        Filtra os dados completos por um intervalo de datas usando um pipeline.

        Args:
            data_inicio (datetime, optional): Data de início do filtro.
            data_fim (datetime, optional): Data de fim do filtro.

        Returns:
            pd.DataFrame: DataFrame com os dados filtrados.
        """
        dados_para_plot = (
            self.dados_completos.copy()
            .pipe(_filtrar_por_data_inicio, data_inicio=data_inicio)
            .pipe(_filtrar_por_data_fim, data_fim=data_fim)
        )
        return dados_para_plot

    def gerar_estatisticas(self, data_inicio=None, data_fim=None):
        """
        Calcula as principais estatísticas para um determinado período.

        Returns:
            tuple: Um dicionário com as estatísticas e o DataFrame filtrado.
        """
        dados_filtrados = self.get_dados_filtrados_para_plot(data_inicio, data_fim)

        if dados_filtrados.empty or dados_filtrados[const.COL_TEMP].isnull().all():
            return {}, dados_filtrados

        temp_array = dados_filtrados[const.COL_TEMP].dropna().values

        estatisticas = {
            "Temperatura Média (°C)": dados_filtrados[const.COL_TEMP].mean(),
            "Umidade Média (%)": dados_filtrados[const.COL_UMIDADE].mean(),
            "Velocidade Média do Vento (km/h)": dados_filtrados[const.COL_VENTO].mean(),
            "Precipitação Total (mm)": dados_filtrados[const.COL_PRECIP].sum(),
            "Desvio Padrão Temp. (°C)": np.std(temp_array) if temp_array.size > 0 else 0,
            "Temperatura (Percentil 25)": np.percentile(temp_array, 25) if temp_array.size > 0 else 0,
            "Temperatura (Percentil 75)": np.percentile(temp_array, 75) if temp_array.size > 0 else 0,
        }
        return estatisticas, dados_filtrados

    def buscar_maiores_indices(self, coluna, n=5):
        """Busca os N dias com os maiores valores para uma coluna."""
        return self.estacao.dias_com_maiores_indices(coluna, n)

    def buscar_menores_indices(self, coluna, n=5):
        """Busca os N dias com os menores valores para uma coluna."""
        return self.estacao.dias_com_menores_indices(coluna, n)

    def gerar_matriz_correlacao(self):
        """Calcula a matriz de correlação para as colunas numéricas dos dados."""
        colunas_numericas = self.dados_completos.select_dtypes(include=['number'])
        return colunas_numericas.corr()

    def gerar_analise_mensal(self, data_inicio=None, data_fim=None):
        """
        Agrupa os dados do período por mês, calculando médias e somas para
        análise sazonal.
        """
        dados_periodo = self.get_dados_filtrados_para_plot(data_inicio, data_fim)
        if dados_periodo.empty:
            return pd.DataFrame()

        analise_mensal = dados_periodo.resample('ME', on=const.COL_DATA).agg({
            const.COL_TEMP: 'mean',
            const.COL_UMIDADE: 'mean',
            const.COL_PRECIP: 'sum'
        }).reset_index()

        analise_mensal = analise_mensal.rename(columns={
            const.COL_TEMP: 'temperatura_media',
            const.COL_UMIDADE: 'umidade_media',
            const.COL_PRECIP: 'precipitacao_total'
        })

        return analise_mensal

    def gerar_resumo_inteligente(self, data_inicio=None, data_fim=None):
        """
        Gera um resumo comparando os dados do período com a média geral 
        """
        estatisticas, dados_filtrados = self.gerar_estatisticas(data_inicio, data_fim)
        if not estatisticas or dados_filtrados.empty:
            return "Não há dados suficientes para gerar um resumo."

        # Médias do período
        temp_periodo = estatisticas['Temperatura Média (°C)']
        umidade_periodo = estatisticas['Umidade Média (%)']
        vento_periodo = estatisticas['Velocidade Média do Vento (km/h)']

        # Médias gerais (históricas)
        media_geral_temp = self.dados_completos[const.COL_TEMP].mean()
        media_geral_umidade = self.dados_completos[const.COL_UMIDADE].mean()
        media_geral_vento = self.dados_completos[const.COL_VENTO].mean()

        # Comparações de Temperatura
        dif_temp = temp_periodo - media_geral_temp
        if dif_temp > 1:
            comp_temp = f"{abs(dif_temp):.1f}°C acima da média (mais quente que o normal)"
        elif dif_temp < -1:
            comp_temp = f"{abs(dif_temp):.1f}°C abaixo da média (mais frio que o normal)"
        else:
            comp_temp = "dentro da normalidade"

        # Comparações de Umidade
        dif_umidade = umidade_periodo - media_geral_umidade
        if dif_umidade > 5:
            comp_umidade = "mais úmido que a média"
        elif dif_umidade < -5:
            comp_umidade = "mais seco que a média"
        else:
            comp_umidade = "dentro da normalidade"

        # Comparações de Vento
        dif_vento = vento_periodo - media_geral_vento
        if dif_vento > 2:
            comp_vento = f"{abs(dif_vento):.1f} km/h acima da média (mais vento que o normal)"
        elif dif_vento < -2:
            comp_vento = f"{abs(dif_vento):.1f} km/h abaixo da média (mais calmo que o normal)"
        else:
            comp_vento = "dentro da normalidade"

        # Dias de extremos no período
        dia_mais_quente = dados_filtrados.loc[dados_filtrados[const.COL_TEMP].idxmax()]
        dia_mais_frio = dados_filtrados.loc[dados_filtrados[const.COL_TEMP].idxmin()]
        dia_mais_vento = dados_filtrados.loc[dados_filtrados[const.COL_VENTO].idxmax()]

        # Montagem do resumo com f-strings formatadas
        resumo = (
            f"Análise do período de {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}:\n\n"
            f" TEMPERATURA:\n"
            f"  - A temperatura média foi de {temp_periodo:,.2f}°C, {comp_temp}.\n"
            f"  - Extremos no período: {dia_mais_quente[const.COL_TEMP]:.1f}°C ({dia_mais_quente[const.COL_DATA].strftime('%d/%m')}) "
            f"e {dia_mais_frio[const.COL_TEMP]:.1f}°C ({dia_mais_frio[const.COL_DATA].strftime('%d/%m')}).\n\n"
            f" VENTO:\n"
            f"  - A velocidade média do vento foi de {vento_periodo:,.2f} km/h, {comp_vento}.\n"
            f"  - A rajada mais forte foi de {dia_mais_vento[const.COL_VENTO]:.1f} km/h em {dia_mais_vento[const.COL_DATA].strftime('%d/%m/%Y')}.\n\n"
            f" UMIDADE E PRECIPITAÇÃO:\n"
            f"  - A umidade média do ar foi de {umidade_periodo:,.2f}%, {comp_umidade}.\n"
            f"  - A precipitação total acumulada no período foi de {estatisticas['Precipitação Total (mm)']:,.2f} mm."
        )
        return resumo