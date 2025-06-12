#!/bin/bash

# Cores para output
VERDE='\033[0;32m'
VERMELHO='\033[0;31m'
AMARELO='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${AMARELO}=== Configuração do PostgreSQL ===${NC}"

# Verifica se o PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo -e "${VERMELHO}PostgreSQL não está instalado. Instalando...${NC}"
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib
else
    echo -e "${VERDE}PostgreSQL já está instalado.${NC}"
fi

# Inicia o serviço do PostgreSQL
echo -e "${AMARELO}Iniciando o serviço do PostgreSQL...${NC}"
sudo service postgresql start

# Configurações do banco de dados
DB_NAME="crud_db"
DB_USER="postgres"
DB_PASSWORD="postgres"

# Cria o banco de dados
echo -e "${AMARELO}Criando banco de dados ${DB_NAME}...${NC}"
sudo -u postgres psql -c "DROP DATABASE IF EXISTS ${DB_NAME};"
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME};"

# Configura a senha do usuário postgres
echo -e "${AMARELO}Configurando senha do usuário postgres...${NC}"
sudo -u postgres psql -c "ALTER USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"

# Cria o arquivo .env
echo -e "${AMARELO}Criando arquivo .env...${NC}"
cat > .env << EOL
DB_HOST=localhost
DB_NAME=${DB_NAME}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_PORT=5432
EOL

echo -e "${VERDE}Configuração concluída com sucesso!${NC}"
echo -e "${AMARELO}Você pode agora executar o programa com:${NC}"
echo -e "${VERDE}python main.py${NC}" 