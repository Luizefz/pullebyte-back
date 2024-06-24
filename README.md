# 🚀 PulleByte Backend

Bem-vindo ao repositório do backend do PulleByte, uma aplicação para otimização e gestão de apostas em ligas de futebol.

Este projeto é desenvolvido exclusivamente com **propósitos educacionais**, como parte dos requisitos para obtenção de nota na disciplina de Desenvolvimento de Sistemas de Informação (DSI).

## 🎯 Objetivos

- **Calendário de Jogos:** Fornece datas, horários e equipes de diversas competições.
- **Gerenciamento de Apostas:** Permite registro, gerenciamento e histórico detalhado das apostas dos usuários.
- **Análises de Apostas:** Oferece insights baseados em desempenho e análises anteriores.

## 🛠️ Tecnologias Utilizadas

- **FastAPI:** Framework para construção de APIs rápidas.
- **httpx:** Para requisições HTTP assíncronas.
- **CORS Middleware:** Configuração para permitir CORS.
- **Python Libraries:** re, json para manipulação de dados.

## 🚀 Instalação e Execução

1. Clone o repositório:
    ```bash
    git clone https://github.com/luizefz/pullebyte-back.git
    cd pullebyte-back
    ```

2. Crie um ambiente virtual e ative:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate  # Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4. Configure as variáveis de ambiente conforme necessário.

5. Inicie a aplicação:
    ```bash
    uvicorn app:app --reload
    ```

## 📋 Endpoints Principais

- **/matches-data:** Dados das partidas.
- **/get_escudo_image/{team_id}:** Imagem do escudo do time.
- **/times:** Dados dos times.

## 📋 Como Contribuir

Se você deseja contribuir com o projeto, siga estes passos:

Faça um fork deste repositório.
Crie uma branch com uma descrição clara do que você está trabalhando (git checkout -b minha-contribuicao).
Faça as alterações desejadas e commit (git commit -am 'feat: Adicionando nova funcionalidade').
Faça push para a branch (git push origin minha-contribuicao).
Abra um pull request explicando suas alterações.

## 📝 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
