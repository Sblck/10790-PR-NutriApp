import re
from modelos.user import User
from persistencia.repositorios import UserRepository


class UserManager:
    """
    Responsável por gerir as regras de negócio relacionadas ao utilizador,
    incluindo validação de dados e verificação de unicidade de email.
    Utiliza o UserRepository para acesso à base de dados de utilizadores.
    """
    def __init__(self, repo: UserRepository):
        """
        Inicializa o gestor de utilizadores com o repositório fornecido.

        :param repo: Instância de UserRepository para acesso à base de dados de utilizadores.
        """
        self.repo = repo


    # TODO : Definir exeptions custom(classes) para projeto

    def __base_user_validation(self, user: User):
        """
        Valida os dados do utilizador fornecido, verificando obrigatoriedade e formato.

        :param user: Instância de User a validar.
        :raises ValueError: Se algum dos dados for inválido (campos obrigatórios, formato de email).
        :return: Uma string que indentifica o tipo de erro, None se os dados são validos
        """
        if not user.is_valid():
            return "missing_fields"
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", user.email):
            return "invalid_email"
        return None
    

    def is_email_unique(self, email: str) -> bool:
        """
        Verifica se o email fornecido ainda não está registado na base de dados.

        :param email: Email a verificar.
        :return: True se o email ainda não existe, False se já está registado.
        """
        return not self.repo.email_exists(email)
    

    def validate_user_for_registration(self, user: User):
        error = self.__base_user_validation(user)
        if error:
            if error == "missing_fields":
                raise ValueError("Campos obrigatórios em falta")
            if error == "invalid_email":
                raise ValueError("Formato de email inválido")
        if not self.is_email_unique(user.email):
            raise ValueError("Email já registado")
        if len(user.password) < 8:
            raise ValueError("Password demasiado curta")
        
    
    def validate_user_for_login(self, user: User):
        error = self.__base_user_validation(user)
        if error:
            raise ValueError("Credenciais inválidas")


    def create_user(self, **user_data) -> User:
        return User(**user_data)

    # outros métodos