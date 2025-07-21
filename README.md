# ProjetoFinal
Um sistema de análise climática , capaz de: Ler e processar dados meteorológicos de arquivos CSV. Realizar análises estatísticas e gerar visualizações. Aplicar conceitos de Programação Orientada a Objetos (POO) . Utilizar Programação Funcional para transformar e filtrar dados. Utilizar Pandas e Numpy para manipulação eficiente dos dados.

Este repositório contém o código-fonte de um projeto de processamento e visualização de dados, focado em analisar informações sobre estações meteorológicas e dados climáticos. O projeto inclui módulos para análise, simulação de estação e visualização de dados.

---

## Ferramentas e Tecnologias Utilizadas

O desenvolvimento deste projeto utilizou as seguintes ferramentas e linguagens:

* **Python 3.10+**: Linguagem de programação principal.
* **Pandas**: Para manipulação e análise de dados tabulares.
* **Matplotlib**: Para a criação de gráficos e visualizações dos dados.
* **Git**: Sistema de controle de versão.
* **GitHub**: Plataforma para hospedagem de código e colaboração.
* **Terminal (Linux/WSL)**: Ambiente de linha de comando utilizado para interagir com o Git e executar o projeto.
* **Nano**: Editor de texto utilizado no terminal para mensagens de commit e merge.
* **VsCode**:  O Visual Studio Code oferece integração nativa com sistemas de controle de versão, como o Git, tornando mais fácil para gerenciar e rastrear as mudanças no código-fonte.
* **CustomTkinter**: Para a personalização da interface.

---

## Processo de Codificação e Desenvolvimento 

O projeto foi desenvolvido seguindo uma abordagem modular, separando as funcionalidades em arquivos Python distintos para melhor organização e manutenção:

2.  **Módulos de Análise e Visualização (Presença de Arquivos):**
    * `analisador.py`: Presumivelmente, contém lógica para processar e extrair insights dos dados.
    * `estacao.py`: Pode simular ou interagir com dados de uma estação meteorológica.
    * `visualizador.py`: Provavelmente responsável por apresentar os dados de forma gráfica ou textual.
    * `utils.py`: Para funções utilitárias e auxiliares reutilizáveis em todo o projeto.
    * `main.py`: O ponto de entrada principal para executar o projeto e suas funcionalidades.

3.  **Gestão de Dados:**
    * Presença de um arquivo `dados/clima.csv` indica o uso de dados CSV para as análises.


4.  **Controle de Versão com Git e GitHub:**
    * Utilização do Git para versionamento do código localmente.
    * Configuração e uso do GitHub como repositório remoto para armazenamento, colaboração e versionamento do projeto na nuvem.
    * Tratamento de configurações de usuário (`git config`), gerenciamento de branches (`git branch`), adição de arquivos (`git add`), gravação de histórico (`git commit`), conexão com repositório remoto (`git remote add`), sincronização (`git pull --allow-unrelated-histories`) e envio de código (`git push`).
    * Inclusão de um arquivo `.gitignore` para exclusão de arquivos temporários e de cache (como a pasta `__pycache__`) do controle de versão.

---

## Como Executar o Projeto (Exemplo)

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/icarolxp/ProjetoFinal.git](https://github.com/icarolxp/ProjetoFinal.git)
    cd ProjetoFinal
    ```
2.  **Instale as dependências:**
    ```bash
    # Exemplo:
    # pip install pandas matplotlib customtkinter

3. **Coloque seu arquivo clima.csv no mesmo diretório do projeto ou ajuste o caminho no app.py.**

4. **Execute a aplicação:**
   ```bash
   python app.py

## 📌 Requisitos
Python 3.8+

Bibliotecas: pandas, matplotlib, customtkinter

---

## 📋 Funcionalidades

- 📅 Listar datas disponíveis no arquivo de dados
- 📊 Exibir estatísticas gerais (média, máxima, mínima)
- 🔥 Listar dias mais quentes
- 💧 Listar dias com maior umidade, vento ou precipitação
- 🔍 Filtrar dados por intervalo de datas
- 📈 Gerar gráficos interativos por variável

## 💾 Formato esperado do arquivo `arquivo.csv`

O arquivo `.csv` deve conter, pelo menos, as seguintes colunas (com variação de nomes aceita, pois o sistema faz normalização):

- `Data`
- `Temperatura (°C)`
- `Umidade (%)`
- `Velocidade do vento (km/h)`
- `Precipitação (mm)`

### Exemplo de conteúdo:

```csv
Data,Temperatura (°C),Umidade (%),Velocidade do vento (km/h),Precipitação (mm)
2025-01-01,32.1,75,10.2,5.0
2025-01-02,31.4,78,8.5,2.3
...

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou sugerir melhorias.

---
