import pandas as pd

class EstacaoMeteorologica:
    def __init__(self, caminho_csv):
        self.df = pd.read_csv(caminho_csv, parse_dates=['data'])

    def filtrar_por_periodo(self, data_inicio, data_fim):
        return self.df[(self.df['data'] >= data_inicio) & (self.df['data'] <= data_fim)]

    def buscar_dias_extremos(self, coluna, n=5, maiores=True):
        return self.df.sort_values(by=coluna, ascending=not maiores).head(n)

    def get_dados(self):
        return self.df.copy()



