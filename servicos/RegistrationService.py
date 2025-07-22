# Responsabilidade: todo o processo de registo

from datetime import date, datetime
from gestores.ProfileManager import ProfileManager
from gestores.UserManager import UserManager
from persistencia.basedados.DataBase import DataBase
from persistencia.repositorios.ObjetivoRepository import ObjetivoRepository
from persistencia.repositorios.PlanoObjetivoRepository import PlanoObjetivoRepository
from persistencia.repositorios.PlanoRepository import PlanoRepository
from persistencia.repositorios.ProfileRepository import ProfileRepository
from persistencia.repositorios.UserRepository import UserRepository
from modelos.plano import Plano
from modelos.planoObjetivo import PlanoObjetivo

class RegistrationService:
    """
    Serviço responsável por orquestrar todo o processo de registo de utilizadores.
    Este serviço coordena a criação e validação de utilizadores, perfis, planos e objetivos iniciais,
    garantindo que todos sejam criados e persistidos de forma consistente.
    O processo inclui validação em memória antes da persistência na base de dados.

    Responsabilidades:
    - Orquestrar o processo completo de registo (utilizador + perfil + plano + objetivo)
    - Validar dados antes da persistência
    - Garantir consistência entre entidades
    - Gerir erros e retornar feedback apropriado
    """
    def __init__(self, db : DataBase, user_manager: UserManager, user_repo: UserRepository, 
                 profile_manager : ProfileManager, profile_repo : ProfileRepository,
                 objetivo_repo : ObjetivoRepository, plano_repo : PlanoRepository, plano_objetivo_repo : PlanoObjetivoRepository):
        """
        Inicializa o RegistrationService com os gestores e repositórios necessários.
        Args:
            db (DataBase):  
            user_manager (UserManager): Gestor para lógica de negócio dos utilizadores
            user_repo (UserRepository): Repositório para persistência de utilizadores
            profile_manager (ProfileManager): Gestor para lógica de negócio dos perfis.
            profile_repo (ProfileRepository): Repositório para persistência de perfis.
            objetivo_repo (ObjetivoRepository): Repositório para objetivos.
            plano_repo (PlanoRepository): Repositório para planos.
            plano_objetivo_repo (PlanoObjetivoRepository): Repositório para objetivos de um plano.
        """
        self.db = db
        self.user_manager = user_manager
        self.user_repo = user_repo
        self.profile_manager = profile_manager
        self.profile_repo = profile_repo
        self.objetivo_repo = objetivo_repo
        self.plano_repo = plano_repo
        self.plano_objetivo_repo = plano_objetivo_repo

    def get_objetivos_disponiveis(self):
        """
        Devolve a lista de objetivos disponíveis para seleção no registo.
        Returns:
            list[Objetivo]: Lista de objetivos disponíveis.
        """
        if not self.objetivo_repo:
            return []
        return self.objetivo_repo.get_all()

    def register_user(self, user_data: dict, profile_data: dict, objetivo_id: int) -> dict:
        """
        Regista um novo utilizador com o seu perfil associado.
        
        Este método executa o processo completo de registo:
        1. Valida se os dados do perfil estão presentes
        2. Cria e valida o utilizador em memória
        3. Cria e valida o perfil em memória
        4. Cria um Plano com base nos objetivos do utlizador
        5. Persiste as entidades na base de dados se não existirem erros
        6. Retorna o resultado da operação
        
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
            objetivo_id (int): Indentificador que define o tipo de bojetivo (existente na base de dados).
                               Exemplo:'perder peso', 'ganhar peso', 'manter peso'
                                        id = 1 , id = 2, id = 3
        
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
            ...     {"nome": "João", "data_nascimento": "1990-01-01", "altura_cm": 175},
            ...     1
            ... )
            >>> print(result)
            {'success': True}
        """
        try:
            
            if not profile_data:
                return {"success": False, "error": "Dados do perfil são obrigatórios."}
            # debug servico
            elif not self.profile_manager:
                return {"success": False, "error": "Sistema gestão de perfil não disponível."}
            elif not self.profile_repo:
                return {"success": False, "error": "Sistema repositório de perfil não disponível."}
            elif not (self.plano_repo and self.plano_objetivo_repo):
                return {"success": False, "error": "Sistema de planos não disponível."}

            # 'YYYY-MM-DD'
            data_inicio = date.today().isoformat()
            # 'YYYY-MM-DD HH:MM:SS'
            data_inicio_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # criar user
            user = self.user_manager.create_user(**user_data)
            # validar user
            self.user_manager.validate_user_for_registration(user)
            # graver e gerar id
            self.user_repo.save_new_user(user)
            
            # criar perfil
            profile_data['data_criacao'] = data_inicio
            profile_data['ultima_atualizacao'] = data_inicio_time
            # atualizar user_id em perfil
            profile_data['user_id'] = user.id
            profile = self.profile_manager.create_profile(**profile_data)

            # validar perfil
            self.profile_manager.validate_profile_for_registration(profile)
            # gravar e gerar id
            self.profile_repo.save_new_profile(profile)

            # criar plano 
            plano = Plano(user_id=user.id, nome="Plano Inicial", data_inicio=data_inicio, estado="ativo")
            self.plano_repo.save_new_plano(plano)

            #objetivo objeto
            plano_objetivo = PlanoObjetivo(plano_id=plano.id, objetivo_id=objetivo_id, data_inicio=data_inicio)

            #gravar e obter id -> tabela sql que liga plano a um objetivo
            self.plano_objetivo_repo.save_new_planoObjetivo(plano_objetivo)

            #adicionar a plano (objeto em memoria)
            #plano.add_objetivo(plano_objetivo=plano_objetivo)

            self.db.connection.commit()
            return {"success": True}
        except ValueError as e:
            self.db.connection.rollback()
            return {"success": False, "error": str(e)}