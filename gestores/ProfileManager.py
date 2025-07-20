from modelos.profile import userProfile
import re

class ProfileManager:
    """
    Responsável por gerir as regras de negócio e validação dos perfis de utilizador + modificações(futuro).
    """
    def create_profile(self, **profile_data):
        """
        Cria e devolve um objeto userProfile.
        
        Args:
            **profile_data: Dicionário com os dados do perfil.
                           Deve conter: user_id, nome, data_nascimento, altura_cm, genero, 
                                      peso_inicial_kg, peso_kg
                           Opcional: data_criacao, ultima_atualizacao
        
        NOTA : As datas de criação e atualização são geridas pela base de dados e só devem ser preenchidas após persistência.
        """
        return userProfile(**profile_data)

    def validate_profile_for_registration(self, profile: userProfile):
        """
        Valida os dados do perfil para registo.
        Lança ValueError com mensagem detalhada se algum campo for inválido.
        """

        if not profile.is_valid():
            raise ValueError("Todos os campos obrigatórios do perfil devem estar preenchidos.")
        if not isinstance(profile.nome, str):
            raise ValueError("Nome deve ser uma string.")
        if not profile.data_nascimento:
            raise ValueError("Data de nascimento é obrigatória.")
        if not isinstance(profile.altura_cm, int) or profile.altura_cm <= 0:
            raise ValueError("Altura deve ser um inteiro positivo (em cm).")
        if not isinstance(profile.genero, str) or len(
            profile.genero)!= 1 or profile.genero not in (
                "M", "F", "O"):
            raise ValueError("Género deve ser 'M', 'F' ou 'O'.")
        if not isinstance(profile.peso_inicial_kg, (int, float)) or profile.peso_inicial_kg <= 0:
            raise ValueError("Peso inicial deve ser um número positivo.")
        if not isinstance(profile.peso_kg, (int, float)) or profile.peso_kg <= 0:
            raise ValueError("Peso atual deve ser um número positivo.")
