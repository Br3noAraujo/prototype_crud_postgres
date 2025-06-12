# 🚀 CRUD PostgreSQL com Python

![Banner do Projeto](https://i.imgur.com/geXVRwr.png)

## 📋 Sobre o Projeto

Este é um sistema CRUD (Create, Read, Update, Delete) desenvolvido em Python com PostgreSQL, oferecendo uma interface amigável e colorida para gerenciamento de usuários.

## ✨ Funcionalidades

- 🆕 Criar novos usuários
- 🔍 Buscar usuários por ID
- 📋 Listar todos os usuários
- ✏️ Atualizar dados de usuários
- 🗑️ Deletar usuários
- 🎨 Interface colorida e intuitiva
- ⚡ Tratamento elegante de interrupções (Ctrl+C)

## 🛠️ Tecnologias Utilizadas

- Python 3.6+
- PostgreSQL
- psycopg2-binary
- python-dotenv

## 🚀 Como Executar

### Pré-requisitos

- Python 3.6 ou superior
- PostgreSQL instalado
- pip (gerenciador de pacotes Python)

### 🔧 Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd prototype_crud_postgres
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados:
```bash
./setup_postgres.sh
```

4. Execute o programa:
```bash
python main.py
```

## 📁 Estrutura do Banco de Dados

A tabela `usuarios` contém os seguintes campos:

| Campo  | Tipo      | Descrição                    |
|--------|-----------|------------------------------|
| id     | SERIAL    | Chave primária autoincremental|
| nome   | VARCHAR   | Nome do usuário              |
| email  | VARCHAR   | Email único do usuário       |
| idade  | INTEGER   | Idade do usuário             |

## 🔐 Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_HOST=localhost
DB_NAME=crud_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
```

## 🎯 Características do Sistema

- 💾 Persistência de dados com PostgreSQL
- 🎨 Interface colorida no terminal
- ⚡ Tratamento de erros robusto
- 🔒 Validação de dados
- 🛑 Encerramento seguro do programa

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---
Desenvolvido com ❤️ por [Seu Nome] 