import pandas as pd
import unicodedata

class EstacaoMeteorologica:
    """
    Classe para carregar e analisar dados de uma estação meteorológica a partir de um arquivo CSV.
    """
    def __init__(self, caminho_csv):
        """
        Inicializa a classe, carrega o DataFrame e normaliza os nomes das colunas.

        Args:
            caminho_csv (str): O caminho para o arquivo CSV com os dados.
        """
        df_original = pd.read_csv(caminho_csv)
        # Normaliza os nomes das colunas para um formato padrão
        df_original.columns = [self._normalizar(col) for col in df_original.columns]
        # Converte a coluna 'data' para o tipo datetime
        df_original["data"] = pd.to_datetime(df_original["data"], errors="coerce")
        self.df = df_original
    def _normalizar(self, nome_coluna):
        """
        Normaliza uma string para um formato de nome de coluna Pythonico.
        - Remove acentos e caracteres especiais.
        - Converte para minúsculas.
        - Substitui espaços e outros caracteres por underscores.
        """
        nome_coluna = nome_coluna.strip().lower()
        nome_coluna = unicodedata.normalize('NFKD', nome_coluna).encode('ASCII', 'ignore').decode('utf-8')
        return nome_coluna.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")

    def get_dados(self):
        """
        Retorna o DataFrame completo com os dados da estação.
        """
        return self.df

    # --- MÉTODOS DE ANÁLISE DE EXTREMOS ---

    def dias_com_maiores_indices(self, coluna, n=5):
        """
        Retorna os N dias com os maiores valores para uma coluna específica.

        Args:
            coluna (str): O nome da coluna a ser analisada.
            n (int, optional): O número de dias a serem retornados. Padrão é 5.

        Returns:
            DataFrame: Um DataFrame contendo a data e os valores dos N dias com maiores índices.
        """
        return self.df.nlargest(n, coluna)[['data', coluna]]

    def dias_com_menores_indices(self, coluna, n=5):
        """
        Retorna os N dias com os menores valores para uma coluna específica.

        Args:
            coluna (str): O nome da coluna a ser analisada.
            n (int, optional): O número de dias a serem retornados. Padrão é 5.

        Returns:
            DataFrame: Um DataFrame contendo a data e os valores dos N dias com menores índices.
        """
        return self.df.nsmallest(n, coluna)[['data', coluna]]
