# API de Exemplo

Este repositório contém uma API desenvolvida com FastAPI. Siga os passos abaixo para configurar e rodar a API localmente.

## Pré-requisitos

Certifique-se de ter o [Docker](https://www.docker.com/get-started) e o [Docker Compose](https://docs.docker.com/compose/install/) instalados em sua máquina.

## Passo a Passo

1. **Instale as dependências do Python:**

   Execute o seguinte comando para instalar as dependências listadas no arquivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt

2. **Construa e inicie os containers Docker:**

   Use o Docker Compose para construir a imagem e iniciar os containers:
   
   ```bash
      docker-compose up --build

4. **Inicie o servidor Uvicorn:**

   Com os containers Docker em execução, inicie o servidor Uvicorn para rodar a aplicação:

       uvicorn main:app --reload
   
    * main:app refere-se ao módulo main e à instância da aplicação app no seu código.
    * O parâmetro --reload faz com que o servidor reinicie automaticamente quando mudanças são detectadas no código.

**Acesso à API**

   Depois de iniciar o servidor, a API estará disponível em http://localhost:8000. Você pode acessar a documentação interativa da API em http://localhost:8000/docs.

**Notas**

  Verifique se os serviços Docker estão funcionando corretamente e que o Docker Compose não apresentou erros durante a construção dos containers.
  Certifique-se de que a porta 8000 está disponível para evitar conflitos.
