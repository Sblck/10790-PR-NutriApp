# Responsabilidade: todo o processo de registo, utilizador + perfil
# criação do utilizador e do perfil em memoria / temp

# TODO : PLANO incial? Objectivo incial ? 


from gestores.ProfileManager import ProfileManager
from gestores.UserManager import UserManager
from persistencia.repositorios.ProfileRepository import ProfileRepository
from persistencia.repositorios.UserRepository import UserRepository


class RegistrationService:
    """
    Serviço responsável por orquestrar todo o processo de registo de utilizadores.
    
    Este serviço coordena a criação e validação de utilizadores e perfis,
    garantindo que ambos sejam criados e persistidos de forma consistente.
    O processo inclui validação em memória antes da persistência na base de dados.
    
    Responsabilidades:
    - Orquestrar o processo completo de registo (utilizador + perfil)
    - Validar dados antes da persistência
    - Garantir consistência entre utilizador e perfil
    - Gerir erros e retornar feedback apropriado
    
    Attributes:
        user_manager (UserManager): Gestor responsável pela lógica de negócio dos utilizadores
        user_repo (UserRepository): Repositório para persistência de utilizadores
        profile_manager (ProfileManager): Gestor responsável pela lógica de negócio dos perfis
        profile_repo (ProfileRepository): Repositório para persistência de perfis
    """
    
    def __init__(self, user_manager: UserManager, user_repo: UserRepository, 
                 profile_manager=ProfileManager, profile_repo=ProfileRepository):
        """
        Inicializa o RegistrationService com os gestores e repositórios necessários.
        
        Args:
            user_manager (UserManager): Gestor para lógica de negócio dos utilizadores
            user_repo (UserRepository): Repositório para persistência de utilizadores
            profile_manager (ProfileManager, optional): Gestor para lógica de negócio dos perfis.
                                                      Defaults to ProfileManager.
            profile_repo (ProfileRepository, optional): Repositório para persistência de perfis.
                                                      Defaults to ProfileRepository.
        """
        self.user_manager = user_manager
        self.user_repo = user_repo
        self.profile_manager = profile_manager
        self.profile_repo = profile_repo


    def register_user(self, user_data: dict, profile_data: dict) -> dict:
        """
        Regista um novo utilizador com o seu perfil associado.
        
        Este método executa o processo completo de registo:
        1. Valida se os dados do perfil estão presentes
        2. Cria e valida o utilizador em memória
        3. Cria e valida o perfil em memória
        4. Persiste ambos na base de dados
        5. Retorna o resultado da operação
        
        Args:
            user_data (dict): Dicionário com os dados do utilizador.
                             Deve conter: email, password
                             Exemplo: {"email": "user@example.com", "password": "secure123"}
            
            profile_data (dict): Dicionário com os dados do perfil.
                                Deve conter: nome, data_nascimento, altura_cm, genero, 
                                           peso_inicial_kg, peso_kg
                                Exemplo: {
                                    "nome": "João Silva",
                                    "data_nascimento": "1990-01-01",
                                    "altura_cm": 175,
                                    "genero": "M",
                                    "peso_inicial_kg": 70.0,
                                    "peso_kg": 70.0
                                }
        
        Returns:
            dict: Dicionário com o resultado da operação.
                  - Em caso de sucesso: {"success": True}
                  - Em caso de erro: {"success": False, "error": "mensagem de erro"}
        
        Raises:
            ValueError: Se os dados do utilizador ou perfil forem inválidos
            Exception: Para outros erros durante o processo de registo
        
        Example:
            >>> service = RegistrationService(user_manager, user_repo, profile_manager, profile_repo)
            >>> result = service.register_user(
            ...     {"email": "user@example.com", "password": "secure123"},
            ...     {"nome": "João", "data_nascimento": "1990-01-01", "altura_cm": 175}
            ... )
            >>> print(result)
            {'success': True}
        """
        try:
            if not profile_data:
                return {"success": False, "error": "Dados do perfil são obrigatórios."}
            
            # criar user temp e validar
            user = self.user_manager.create_user(**user_data)
            self.user_manager.validate_user_for_registration(user)
            
            # debug servico
            if not self.profile_manager:
                return {"success": False, "error": "Sistema de perfil não disponível."}
            
            # criar perfil temp e validar
            profile = self.profile_manager.create_profile(**profile_data)
            self.profile_manager.validate_profile_for_registration(profile)

            # transformar user temp em user final e perfil temp em perfil final -> gravar db
            self.user_repo.save_new_user(user)
            if not self.profile_repo:
                return {"success": False, "error": "Sistema de perfil não disponível."}
            # atualizar a chave estrangeira user_id em perfil que aponta para o utilizador válido
            profile.user_id= user.id
            self.profile_repo.save_new_profile(profile)
            return {"success": True}
        
        except ValueError as e:
            return {"success": False, "error": str(e)}