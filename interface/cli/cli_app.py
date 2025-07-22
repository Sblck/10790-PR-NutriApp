from modelos import user

'''

Main app

'''
class CLIApp:
    def __init__(self, plano_service=None, plano_objetivo_service=None, profile_service=None):
        self.plano_service = plano_service
        self.plano_objetivo_service = plano_objetivo_service
        self.profile_service = profile_service

    def execute(self, session):
        print(f"Bem-vindo! {session.user.email}!")
        # Buscar perfil, plano e objetivo correntes
        profile = session.profile
        plano_ativo = session.plano
        objetivo_corrente = session.objetivo

        print("\n--- Dados Correntes ---")
        print(f"Perfil: {profile.nome} ({profile.data_nascimento})")
        if plano_ativo:
            print(f"Plano atual: {plano_ativo.nome} (Estado: {plano_ativo.estado})")
        else:
            print("Sem plano ativo.")
        if objetivo_corrente:
            print(f"Objetivo atual: {objetivo_corrente.nome}")
        else:
            print("Sem objetivo ativo.")

