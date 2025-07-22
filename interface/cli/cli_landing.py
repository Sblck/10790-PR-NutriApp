from servicos.AuthService import AuthService
from servicos.RegistrationService import RegistrationService

'''
Interface "landing"

'''
class CLILanding:
    def __init__(self, auth_service: AuthService, registration_service: RegistrationService):
        self.auth_service = auth_service
        self.registration_service = registration_service


    def execute(self):
        while True:
            print("\n=== Autenticação ===")
            print("1. Login")
            print("2. Registar")
            print("3. Sair")
            op = input("Opção: ")
            if op == "1":
                user = self.login()
                # autenticar após login
                if user:
                    return user 
            elif op == "2":
                user = self.register()
                # autenticar após registo
                if user:
                    return user  
            elif op == "3":
                return None
            else:
                print("Opção inválida.")


    def __get_credentials(self, titulo):
        """
        Método para recolher email e password.
        Retorna um dicionário com as credenciais ou None se o utilizador cancelar.
        """
        print(f"\n### {titulo} ###")
        print("(Deixe o email vazio para voltar ao menu de autenticação)")
        
        email = input("Email: ")
        if email.strip() == "":
            return None
        password = input("Password: ")
        
        return {
            "email": email,
            "password": password
        }


    def login(self):
        while True:
            credentials = self.__get_credentials("Login Utilizador")
            if credentials is None:
                return None
                
            try:
                user = self.auth_service.login(credentials["email"], credentials["password"])
                if user is None:
                    continue
                print(f"Log-in efetuado com sucesso!! {user.email}!")
                return user
            except ValueError as e:
                print("Erro:", str(e))

    
    def register(self):
        while True:
            # recolher credenciais
            credentials = self.__get_credentials("Registo Utilizador")
            if credentials is None:
                return None
            
            # recolher dados do perfil
            profile_data = self.__get_profile_data()
            if profile_data is None:
                continue
            objetivo_id = self.__choose_objetivo()
            if objetivo_id is None:
                print("Registo cancelado.")
                return None
            user_data = credentials
            try:
                result = self.registration_service.register_user(user_data, profile_data, objetivo_id)
                if result["success"]:
                    print("Registo efetuado com sucesso!")
                    return self.auth_service.login(credentials["email"], credentials["password"])
                else:
                    print("Erro no registo:", result["error"])
                    if not self.__ask_retry():
                        return None
                    continue
            except (ValueError, Exception) as e:
                print("Erro:", str(e))
                if not self.__ask_retry():
                    return None
                continue


    def __get_profile_data(self):
        """
        Recolhe os dados do perfil com validação individual.
        Retorna um dicionário com os dados ou None se o utilizador cancelar.
        """
        print("\n--- Dados do Perfil ---")
        print("(Deixe o nome vazio para voltar ao menu de autenticação)")
        
        while True:
            nome = input("Nome: ").strip()
            if nome == "":
                return None
            
            data_nascimento = input("Data de nascimento (YYYY-MM-DD): ").strip()
            if not data_nascimento:
                print("Data de nascimento é obrigatória.")
                continue
            
            try:
                altura_cm = input("Altura (cm): ").strip()
                if not altura_cm:
                    print("Altura é obrigatória.")
                    continue
                altura_cm = int(altura_cm)
                if altura_cm <= 0:
                    print("Altura deve ser um número positivo.")
                    continue
            except ValueError:
                print("Altura deve ser um número inteiro.")
                continue
            
            genero = input("Género (M/F/O): ").strip().upper()
            if genero not in ['M', 'F', 'O']:
                print("Género deve ser M, F ou O.")
                continue
            
            try:
                peso_kg = input("Peso atual (kg): ").strip()
                if not peso_kg:
                    print("Peso atual é obrigatório.")
                    continue
                # primeiro registo peso atual = peso inicial
                peso_kg = float(peso_kg)
                peso_inicial_kg = peso_kg
                if peso_kg <= 0:
                    print("Peso atual deve ser um número positivo.")
                    continue
            except ValueError:
                print("Peso atual deve ser um número.")
                continue
            
            #  chegou aqui, todos os dados estao ok
            return {
                "nome": nome,
                "data_nascimento": data_nascimento,
                "altura_cm": altura_cm,
                "genero": genero,
                "peso_inicial_kg": peso_inicial_kg,
                "peso_kg": peso_kg
            }
        
    
    def __choose_objetivo(self):
        objetivos = self.registration_service.get_objetivos_disponiveis()
        if not objetivos:
            print("Nenhum objetivo disponível. Contacte o administrador.")
            return None
        print("\n--- Escolha o seu objetivo inicial ---")
        for idx, obj in enumerate(objetivos, 1):
            print(f"{idx}. {obj.nome}")
        while True:
            escolha = input("Selecione o número do objetivo: ").strip()
            if not escolha.isdigit() or not (1 <= int(escolha) <= len(objetivos)):
                print("Opção inválida. Tente novamente.")
                continue
            return objetivos[int(escolha)-1].id


    def __ask_retry(self):
        """
        Pergunta ao utilizador se quer tentar novamente.
        Retorna True se sim, False se não.
        """
        while True:
            retry = input("\nDeseja tentar novamente? (s/n): ").strip().lower()
            if retry in ['s', 'sim', 'y', 'yes']:
                return True
            elif retry in ['n', 'não', 'nao', 'no']:
                return False
            else:
                print("Por favor, responda 's' para sim ou 'n' para não.")