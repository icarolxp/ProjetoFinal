import numpy as np

class AnalisadorDeDados:
    def __init__(self, df):
        self.df = df

    def temperatura_estatisticas(self):
        
        return {
            'media': self.df['temperatura'].mean(),
            'minima': self.df['temperatura'].min(),
            'maxima': self.df['temperatura'].max()
        }

    def dias_com_chuva(self, limite_mm):
        return self.df[self.df['precipitacao'] > limite_mm]

    def umidade_estatisticas(self):
        return {
            'media': self.df['umidade'].mean(),
            'desvio_padrao': np.std(self.df['umidade'])
        }

    def media_vento(self):
        return self.df['vento'].mean()

