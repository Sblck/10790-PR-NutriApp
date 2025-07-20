import traceback


class CLIMain:
    def __init__(self, cli_auth, cli_app):
        self.cli_auth = cli_auth
        self.cli_app = cli_app
        self.current_user = None


    def run(self):
        while True:
            try:
                user = self.cli_auth.execute()
                if user is None:
                    print("A sair da aplicação...")
                    break
                self.current_user = user
                # correr menu_principal da applicação em si | fim do processo de autenticação
                self.cli_app.execute(self.current_user)
            except Exception as e:
                traceback.print_exc()

