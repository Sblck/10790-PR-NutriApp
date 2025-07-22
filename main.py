'''
Entrada da app
'''
import os
from interface.cli.cli_app import CLIApp
from interface.cli.cli_landing import CLILanding
from persistencia.basedados.DataBase import DataBase
from persistencia.repositorios.ObjetivoRepository import ObjetivoRepository
from persistencia.repositorios.PlanoObjetivoRepository import PlanoObjetivoRepository
from persistencia.repositorios.PlanoRepository import PlanoRepository
from servicos.AuthService import AuthService
from servicos.RegistrationService import RegistrationService
from servicos.UserService import UserService
from servicos.PlanoService import PlanoService
from servicos.PlanoObjetivoService import PlanoObjetivoService
from gestores.UserManager import UserManager
from gestores.ProfileManager import ProfileManager
from persistencia.repositorios.UserRepository import UserRepository
from persistencia.repositorios.ProfileRepository import ProfileRepository
from interface.cli.cli_main import CLIMain
# (Opcional) ProfileService

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

    # seed objetivos
    def seed_objetivos(db):
        objetivos = ['perder peso', 'ganhar peso', 'manter peso']
        for nome in objetivos:
            db.execute(
                "INSERT IGNORE INTO objetivo (nome) VALUES (%s)", (nome,)
            )
        print("Objetivos base inseridos/atualizados.")

    # popular os objetivos
    try:
        seed_objetivos(db)
        db.connection.commit()
    except Exception as e:
        db.connection.rollback()
        print("Erro ao inserir objetivos base:", e)

    return db  # retorna a instância para ser usada no resto da app

def main():
    # init da BD, repos, managers, services etc
    db = init()
    
    # utilizador
    user_repo = UserRepository(db)
    user_manager = UserManager(user_repo)
    user_service = UserService(user_repo, user_manager)

    # perfil
    profile_repo = ProfileRepository(db)
    profile_manager = ProfileManager()

    # objetivo
    objetivo_repo = ObjetivoRepository(db)

    # plano
    plano_repo = PlanoRepository(db)
    plano_service = PlanoService(plano_repo)

    # plano_objetivo
    plano_objetivo_repo = PlanoObjetivoRepository(db)
    plano_objetivo_service = PlanoObjetivoService(plano_objetivo_repo, objetivo_repo)

    # operaçoes
    auth_service = AuthService(user_manager=user_manager,user_repo=user_repo)
    registration_service = RegistrationService(
        db=db,
        user_manager=user_manager,
        user_repo=user_repo,
        profile_manager=profile_manager,
        profile_repo=profile_repo,
        objetivo_repo=objetivo_repo,
        plano_repo=plano_repo,
        plano_objetivo_repo=plano_objetivo_repo
    )

    # interfaces cli
    cli_auth = CLILanding(auth_service=auth_service,registration_service=registration_service)
    cli_app = CLIApp(plano_service=plano_service, plano_objetivo_service=plano_objetivo_service, profile_service=None)

    #Main loop interface
    cli = CLIMain(cli_auth, cli_app, plano_service, plano_objetivo_service, profile_service=None, tempProfileRepo=profile_repo)

    # fluxo da aplicação princiapl (auth, menus etc)
    cli.run()

    
    
    #cli_profile = CLIProfile(user_service, profile_service)



    # ...

if __name__ == "__main__":
    main()