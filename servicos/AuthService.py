from gestores.UserManager import UserManager
from persistencia.repositorios.UserRepository import UserRepository


class AuthService:
    """
    Serviço responsável por autenticação de utilizadores.
    """
    def __init__(self, user_manager: UserManager, user_repo: UserRepository):
        self.user_manager = user_manager
        self.user_repo = user_repo


    def login(self, email: str, password: str):
        """
        Autentica um utilizador com base no email e password fornecidos.

        :param email: Email do utilizador.
        :param password: Password do utilizador.
        :raises ValueError: Se os dados forem inválidos.
        :return: Instância de User autenticado, ou None se as credenciais estiverem incorretas.
        """
        user_data = {"email": email, "password": password}
        user = self.user_manager.create_user(**user_data)
        try:
            self.user_manager.validate_user_for_login(user)
            user_db = self.user_repo.get_user(email, password)
            if not user_db:
                raise ValueError("Credenciais inválidas")
            return user_db
        except ValueError:
            raise ValueError("Credenciais inválidas")


    def logout():
        pass
