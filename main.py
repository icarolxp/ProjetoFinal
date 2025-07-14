from estacao import EstacaoMeteorologica
from analisador import AnalisadorDeDados
from visualizador import Visualizador
from utils import filtrar_dias_quentes, somar_precipitacao
import matplotlib.pyplot as plt

def main():
    estacao = EstacaoMeteorologica('dados/clima.csv')
    dados = estacao.get_dados()

    analisador = AnalisadorDeDados(dados)
    print("Temperatura (média, min, max):", analisador.temperatura_estatisticas())
    print("Umidade (média, desvio):", analisador.umidade_estatisticas())
    print("Velocidade média do vento:", analisador.media_vento())

    print("\nDias com chuva acima de 10mm:")
    print(analisador.dias_com_chuva(10)[['data', 'precipitacao']])

    dias_extremos = estacao.buscar_dias_extremos('temperatura', maiores=True)
    print("\nTop 5 dias mais quentes:")
    print(dias_extremos[['data', 'temperatura']])

    # Visualizações

    Visualizador.linha_temperatura(dados)
    Visualizador.histograma_umidade(dados)
    plt.show()

    # Parte funcional
    quentes = filtrar_dias_quentes(dados)
    print(f"\nDias com temperatura acima de 30°C: {len(quentes)}")

    total_precipitacao = somar_precipitacao(dados)
    print(f"Total de precipitação: {total_precipitacao:.1f} mm")


if __name__ == "__main__":
    main()
    
    

