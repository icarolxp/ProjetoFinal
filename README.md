# ProjetoFinal
Um sistema de análise climática , capaz de: Ler e processar dados meteorológicos de arquivos CSV. Realizar análises estatísticas e gerar visualizações. Aplicar conceitos de Programação Orientada a Objetos (POO) . Utilizar Programação Funcional para transformar e filtrar dados. Utilizar Pandas e Numpy para manipulação eficiente dos dados.

Este repositório contém o código-fonte de um projeto de processamento e visualização de dados, focado em analisar informações sobre estações meteorológicas e dados climáticos. O projeto inclui módulos para análise, simulação de estação e visualização de dados.

---

## Ferramentas e Tecnologias Utilizadas

O desenvolvimento deste projeto utilizou as seguintes ferramentas e linguagens:

* **Python 3.10+**: Linguagem de programação principal.
* **Hashlib (SHA256)**: Para calcular hashes e garantir a integridade dos blocos de dados.
* **Pandas**: Para manipulação e análise de dados tabulares.
* **Matplotlib**: Para a criação de gráficos e visualizações dos dados.
* **Git**: Sistema de controle de versão.
* **GitHub**: Plataforma para hospedagem de código e colaboração.
* **Terminal (Linux/WSL)**: Ambiente de linha de comando utilizado para interagir com o Git e executar o projeto.
* **Nano**: Editor de texto utilizado no terminal para mensagens de commit e merge.

---

## 👨‍💻 Processo de Codificação e Desenvolvimento

O projeto foi desenvolvido seguindo uma abordagem modular, separando as funcionalidades em arquivos Python distintos para melhor organização e manutenção:

1.  **Estrutura de Dados (Blocos):** Implementação de uma estrutura simples de "bloco" com dados, timestamp, hash anterior e seu próprio hash.
    * `criar_bloco()`: Função para construir um novo bloco.
    * `calcular_hash()`: Função para gerar o hash SHA256 de um bloco.

2.  **Módulo P2P Simplificado:**
    * Configuração de um servidor para escutar conexões de outros peers.
    * Funções para conectar a peers externos.
    * `handle_client()` e `receive_messages()`: Funções multithreaded para gerenciar o recebimento de mensagens (blocos) de peers conectados.
    * `broadcast_bloco()`: Funcionalidade para propagar blocos recém-criados para todos os peers conectados, simulando a distribuição em uma rede blockchain.

3.  **Módulos de Análise e Visualização (Presença de Arquivos):**
    * `analisador.py`: Presumivelmente, contém lógica para processar e extrair insights dos dados.
    * `estacao.py`: Pode simular ou interagir com dados de uma estação meteorológica.
    * `visualizador.py`: Provavelmente responsável por apresentar os dados de forma gráfica ou textual.
    * `utils.py`: Para funções utilitárias e auxiliares reutilizáveis em todo o projeto.
    * `main.py`: O ponto de entrada principal para executar o projeto e suas funcionalidades.

4.  **Gestão de Dados:**
    * Presença de um arquivo `dados/clima.csv` indica o uso de dados CSV para as análises.
    * A pasta `.ipynb_checkpoints` sugere uma fase de exploração e prototipagem de dados utilizando Jupyter Notebooks.

5.  **Controle de Versão com Git e GitHub:**
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
2.  **Instale as dependências (se houver, adicione um `requirements.txt`):**
    ```bash
    # Exemplo:
    # pip install pandas matplotlib
    ```
3.  **Execute o peer (no terminal):**
    ```bash
    python main.py
    ```
    Ou inicie cada módulo conforme sua estrutura.

    Para o módulo P2P, você iniciaria o peer e depois conectaria a outros peers conforme a lógica do `main.py`:
    ```bash
    # Exemplo de interação no terminal após iniciar main.py
    # Digite a porta para este peer: 8000
    # Comandos: conectar <host> <porta> | bloco <dados> | sair
    # >>> conectar localhost 8001
    # >>> bloco Minha primeira transacao
    ```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou sugerir melhorias.

---
