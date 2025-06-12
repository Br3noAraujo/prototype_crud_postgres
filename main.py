import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import signal
import sys

# Carrega as variáveis de ambiente
load_dotenv()

# Cores para o terminal
class Cores:
    # Cores principais
    AZUL = '\033[94m'
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    ROXO = '\033[95m'
    CIANO = '\033[96m'
    
    # Estilos
    NEGRITO = '\033[1m'
    
    # Reset
    RESET = '\033[0m'
    
    # Combinações
    TITULO = f"{NEGRITO}{AZUL}"
    SUCESSO = f"{NEGRITO}{VERDE}"
    ERRO = f"{NEGRITO}{VERMELHO}"
    ALERTA = f"{NEGRITO}{AMARELO}"
    DESTAQUE = f"{NEGRITO}{ROXO}"
    INFO = f"{NEGRITO}{CIANO}"

class Database:
    def __init__(self):
        self.conn = None
        self.cur = None
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "crud_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "postgres"),
                port=os.getenv("DB_PORT", "5432")
            )
            self.cur = self.conn.cursor()
            
            # Cria a tabela se não existir
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    idade INTEGER
                )
            """)
            self.conn.commit()
            
        except Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            if self.conn:
                self.conn.close()
            raise Exception("Não foi possível conectar ao banco de dados. Verifique suas configurações.")

    def criar_usuario(self, nome, email, idade):
        if not self.cur:
            raise Exception("Conexão com o banco de dados não estabelecida.")
        try:
            self.cur.execute(
                "INSERT INTO usuarios (nome, email, idade) VALUES (%s, %s, %s) RETURNING id",
                (nome, email, idade)
            )
            self.conn.commit()
            return self.cur.fetchone()[0]
        except Error as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    def buscar_usuario(self, id):
        if not self.cur:
            raise Exception("Conexão com o banco de dados não estabelecida.")
        try:
            self.cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
            return self.cur.fetchone()
        except Error as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

    def listar_usuarios(self):
        if not self.cur:
            raise Exception("Conexão com o banco de dados não estabelecida.")
        try:
            self.cur.execute("SELECT * FROM usuarios")
            return self.cur.fetchall()
        except Error as e:
            print(f"Erro ao listar usuários: {e}")
            return []

    def atualizar_usuario(self, id, nome=None, email=None, idade=None):
        if not self.cur:
            raise Exception("Conexão com o banco de dados não estabelecida.")
        try:
            updates = []
            values = []
            if nome:
                updates.append("nome = %s")
                values.append(nome)
            if email:
                updates.append("email = %s")
                values.append(email)
            if idade:
                updates.append("idade = %s")
                values.append(idade)
            
            if not updates:
                return False
                
            values.append(id)
            query = f"UPDATE usuarios SET {', '.join(updates)} WHERE id = %s"
            self.cur.execute(query, tuple(values))
            self.conn.commit()
            return True
        except Error as e:
            print(f"Erro ao atualizar usuário: {e}")
            return False

    def deletar_usuario(self, id):
        if not self.cur:
            raise Exception("Conexão com o banco de dados não estabelecida.")
        try:
            self.cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            self.conn.commit()
            return True
        except Error as e:
            print(f"Erro ao deletar usuário: {e}")
            return False

    def __del__(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    print(f"\n{Cores.TITULO}Sistema de Gerenciamento de Usuários{Cores.RESET}")
    print(f"{Cores.INFO}1. Criar novo usuário{Cores.RESET}")
    print(f"{Cores.INFO}2. Buscar usuário por ID{Cores.RESET}")
    print(f"{Cores.INFO}3. Listar todos os usuários{Cores.RESET}")
    print(f"{Cores.INFO}4. Atualizar usuário{Cores.RESET}")
    print(f"{Cores.INFO}5. Deletar usuário{Cores.RESET}")
    print(f"{Cores.INFO}0. Sair{Cores.RESET}")
    return input(f"\n{Cores.INFO}Escolha uma opção: {Cores.RESET}")

def criar_novo_usuario(db):
    print(f"\n{Cores.TITULO}Criar Novo Usuário{Cores.RESET}")
    nome = input(f"{Cores.INFO}Digite o nome: {Cores.RESET}")
    email = input(f"{Cores.INFO}Digite o email: {Cores.RESET}")
    while True:
        try:
            idade = int(input(f"{Cores.INFO}Digite a idade: {Cores.RESET}"))
            break
        except ValueError:
            print(f"{Cores.ERRO}Por favor, digite um número válido para a idade.{Cores.RESET}")
    
    user_id = db.criar_usuario(nome, email, idade)
    if user_id:
        print(f"\n{Cores.SUCESSO}Usuário criado com sucesso! ID: {user_id}{Cores.RESET}")
    else:
        print(f"\n{Cores.ERRO}Erro ao criar usuário. Verifique se o email já está em uso.{Cores.RESET}")
    input(f"\n{Cores.INFO}Pressione Enter para continuar...{Cores.RESET}")

def buscar_usuario_por_id(db):
    print(f"\n{Cores.TITULO}Buscar Usuário por ID{Cores.RESET}")
    try:
        id = int(input(f"{Cores.INFO}Digite o ID do usuário: {Cores.RESET}"))
        usuario = db.buscar_usuario(id)
        if usuario:
            print(f"\n{Cores.SUCESSO}Usuário encontrado:{Cores.RESET}")
            print(f"{Cores.INFO}ID: {Cores.RESET}{usuario[0]}")
            print(f"{Cores.INFO}Nome: {Cores.RESET}{usuario[1]}")
            print(f"{Cores.INFO}Email: {Cores.RESET}{usuario[2]}")
            print(f"{Cores.INFO}Idade: {Cores.RESET}{usuario[3]}")
        else:
            print(f"\n{Cores.ERRO}Usuário não encontrado.{Cores.RESET}")
    except ValueError:
        print(f"\n{Cores.ERRO}Por favor, digite um ID válido.{Cores.RESET}")
    input(f"\n{Cores.INFO}Pressione Enter para continuar...{Cores.RESET}")

def listar_todos_usuarios(db):
    print(f"\n{Cores.TITULO}Lista de Todos os Usuários{Cores.RESET}")
    usuarios = db.listar_usuarios()
    if usuarios:
        for usuario in usuarios:
            print(f"\n{Cores.DESTAQUE}Usuário:{Cores.RESET}")
            print(f"{Cores.INFO}ID: {Cores.RESET}{usuario[0]}")
            print(f"{Cores.INFO}Nome: {Cores.RESET}{usuario[1]}")
            print(f"{Cores.INFO}Email: {Cores.RESET}{usuario[2]}")
            print(f"{Cores.INFO}Idade: {Cores.RESET}{usuario[3]}")
            print(f"{Cores.DESTAQUE}{'─' * 30}{Cores.RESET}")
    else:
        print(f"\n{Cores.ALERTA}Nenhum usuário cadastrado.{Cores.RESET}")
    input(f"\n{Cores.INFO}Pressione Enter para continuar...{Cores.RESET}")

def atualizar_usuario(db):
    print(f"\n{Cores.TITULO}Atualizar Usuário{Cores.RESET}")
    try:
        id = int(input(f"{Cores.INFO}Digite o ID do usuário que deseja atualizar: {Cores.RESET}"))
        usuario = db.buscar_usuario(id)
        if usuario:
            print(f"\n{Cores.INFO}Usuário atual:{Cores.RESET}")
            print(f"{Cores.INFO}Nome: {Cores.RESET}{usuario[1]}")
            print(f"{Cores.INFO}Email: {Cores.RESET}{usuario[2]}")
            print(f"{Cores.INFO}Idade: {Cores.RESET}{usuario[3]}")
            print(f"\n{Cores.ALERTA}Deixe em branco os campos que não deseja alterar.{Cores.RESET}")
            
            nome = input(f"\n{Cores.INFO}Novo nome (Enter para manter): {Cores.RESET}")
            email = input(f"{Cores.INFO}Novo email (Enter para manter): {Cores.RESET}")
            idade_str = input(f"{Cores.INFO}Nova idade (Enter para manter): {Cores.RESET}")
            
            nome = nome if nome else None
            email = email if email else None
            idade = int(idade_str) if idade_str else None
            
            if db.atualizar_usuario(id, nome, email, idade):
                print(f"\n{Cores.SUCESSO}Usuário atualizado com sucesso!{Cores.RESET}")
            else:
                print(f"\n{Cores.ERRO}Erro ao atualizar usuário.{Cores.RESET}")
        else:
            print(f"\n{Cores.ERRO}Usuário não encontrado.{Cores.RESET}")
    except ValueError:
        print(f"\n{Cores.ERRO}Por favor, digite valores válidos.{Cores.RESET}")
    input(f"\n{Cores.INFO}Pressione Enter para continuar...{Cores.RESET}")

def deletar_usuario(db):
    print(f"\n{Cores.TITULO}Deletar Usuário{Cores.RESET}")
    try:
        id = int(input(f"{Cores.INFO}Digite o ID do usuário que deseja deletar: {Cores.RESET}"))
        usuario = db.buscar_usuario(id)
        if usuario:
            print(f"\n{Cores.INFO}Usuário encontrado:{Cores.RESET}")
            print(f"{Cores.INFO}Nome: {Cores.RESET}{usuario[1]}")
            print(f"{Cores.INFO}Email: {Cores.RESET}{usuario[2]}")
            print(f"{Cores.INFO}Idade: {Cores.RESET}{usuario[3]}")
            
            confirmacao = input(f"\n{Cores.ALERTA}Tem certeza que deseja deletar este usuário? (s/N): {Cores.RESET}")
            if confirmacao.lower() == 's':
                if db.deletar_usuario(id):
                    print(f"\n{Cores.SUCESSO}Usuário deletado com sucesso!{Cores.RESET}")
                else:
                    print(f"\n{Cores.ERRO}Erro ao deletar usuário.{Cores.RESET}")
            else:
                print(f"\n{Cores.ALERTA}Operação cancelada.{Cores.RESET}")
        else:
            print(f"\n{Cores.ERRO}Usuário não encontrado.{Cores.RESET}")
    except ValueError:
        print(f"\n{Cores.ERRO}Por favor, digite um ID válido.{Cores.RESET}")
    input(f"\n{Cores.INFO}Pressione Enter para continuar...{Cores.RESET}")

def sair_graciosamente(signum, frame):
    print(f"\n\n{Cores.ALERTA}⚠️  Interrupção detectada!{Cores.RESET}")
    print(f"{Cores.INFO}Encerrando o programa de forma segura...{Cores.RESET}")
    
    # Aqui você pode adicionar qualquer limpeza necessária
    # Por exemplo, fechar conexões com o banco de dados
    
    print(f"{Cores.SUCESSO}Programa encerrado com sucesso!{Cores.RESET}")
    sys.exit(0)

def main():
    # Registra o handler para Ctrl+C
    signal.signal(signal.SIGINT, sair_graciosamente)
    
    try:
        db = Database()
        
        while True:
            limpar_tela()
            opcao = exibir_menu()
            
            if opcao == "1":
                criar_novo_usuario(db)
            elif opcao == "2":
                buscar_usuario_por_id(db)
            elif opcao == "3":
                listar_todos_usuarios(db)
            elif opcao == "4":
                atualizar_usuario(db)
            elif opcao == "5":
                deletar_usuario(db)
            elif opcao == "0":
                print(f"\n{Cores.SUCESSO}Saindo do sistema...{Cores.RESET}")
                break
            else:
                print(f"\n{Cores.ERRO}Opção inválida!{Cores.RESET}")
                input(f"{Cores.INFO}Pressione Enter para continuar...{Cores.RESET}")
    except Exception as e:
        print(f"\n{Cores.ERRO}Erro ao iniciar o sistema: {str(e)}{Cores.RESET}")
        input(f"{Cores.INFO}Pressione Enter para sair...{Cores.RESET}")
    finally:
        # Garante que a conexão com o banco de dados seja fechada
        if 'db' in locals():
            db.__del__()

if __name__ == "__main__":
    main()
