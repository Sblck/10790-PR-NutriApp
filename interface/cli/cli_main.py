import traceback

from modelos.userSession import UserSession


class CLIMain:
    def __init__(self, cli_auth, cli_app, plano_service, plano_objetivo_service, profile_service=None, tempProfileRepo = None):
        self.cli_auth = cli_auth
        self.cli_app = cli_app
        self.profile_service = profile_service
        self.plano_service = plano_service
        self.plano_objetivo_service = plano_objetivo_service
        self.current_session = None
        # todo : remove (temp para teste)
        self.profile_repo = tempProfileRepo

    def run(self):
        while True:
            try:
                user = self.cli_auth.execute()
                if user is None:
                    print("A sair da aplicação...")
                    break
                # perfil, plano e objetivo do utilizador autenticado
                #profile = self.profile_service.get_profile_by_user_id(user.id)
                profile = self.profile_repo.get_profile_by_user_id(user.id)
                plano = self.plano_service.get_plano_ativo(user.id)
                objetivo = self.plano_objetivo_service.get_objetivo_ativo(plano.id) if plano else None
                # criar objeto que mantem user + dados  UserSession
                session = UserSession(user=user, profile=profile, plano=plano, objetivo=objetivo)
                self.current_session = session
                # passar objeto UserSession para a app principal
                self.cli_app.execute(session)
            except Exception as e:
                traceback.print_exc()

