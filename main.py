'''
Entrada da app
'''
import os
from persistencia.basedados.DataBase import DataBase

# NOTA : Consultar o diagrama : Processo de inicialização
def init():
    # verificar se config.ini existe
    if not os.path.exists('config.ini'):
        print("Ficheiro config.ini não encontrado. Por favor, crie e preencha com as suas credenciais.")
        exit(1)

    # init DataBase (carrega config)
    try:
        db = DataBase()
    except FileNotFoundError as fnf:
        print(f"Erro: {fnf}")
        exit(1)
    except KeyError as ke:
        print(f"Erro de configuração: {ke}")
        print("Por favor, verifique se o ficheiro config.ini tem a secção [database] e todas as chaves necessárias (host, user, password, dbname).")
        exit(1)
    except Exception as e:
        print(f"Erro inesperado ao carregar configuração: {e}")
        exit(1)

    # criar base de dados se não existir
    try:
        db.create_database_if_not_exists()
    except Exception as error:
        print("Não foi possível criar/verificar a base de dados.", error)
        exit(1)

    # conectar a base de dados
    try:
        db.connect_to_data_base()
    except Exception as error:
        print("Não foi possível conectar à base de dados.", error)
        exit(1)

    # criar tabelas se necessário
    db.create_tables()

    return db  # retorna a instância para ser usada no resto da app

def main():
    db = init()

    # fluxo da aplicação princiapl (menus, auth, etc)
    # ex: mostrar_menu_principal(db)
    # ...

if __name__ == "__main__":
    main()