import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Visualizador:
    @staticmethod
    def linha_temperatura(df, salvar=False):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df['data'], df['temperatura'], color='orange', marker='o', linestyle='-')

        ax.set_title('📈 Temperatura ao Longo do Tempo', fontsize=14)
        ax.set_xlabel('Data', fontsize=12)
        ax.set_ylabel('Temperatura (°C)', fontsize=12)
        ax.grid(True)

        # Melhorar formato das datas no eixo x
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
        fig.autofmt_xdate()

        if salvar:
            fig.savefig("grafico_temperatura.png", dpi=300)

    @staticmethod
    def histograma_umidade(df, salvar=False):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(df['umidade'], bins=10, color='blue', edgecolor='black')

        ax.set_title('🌧️ Distribuição da Umidade Relativa (%)', fontsize=14)
        ax.set_xlabel('Umidade (%)', fontsize=12)
        ax.set_ylabel('Frequência', fontsize=12)
        ax.grid(True)

        if salvar:
            fig.savefig("grafico_umidade.png", dpi=300)
