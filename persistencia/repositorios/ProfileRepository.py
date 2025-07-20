from typing import Optional
from modelos.profile import userProfile
from persistencia.basedados.DataBase import DataBase

class ProfileRepository:
    def __init__(self, db: DataBase):
        """
        Repositório responsável pelas operações relacionadas ao perfil de utilizador.
        Recebe uma instância da classe DataBase para acesso centralizado à base de dados e seus métodos.
        """
        self.db = db


    def save_new_profile(self, profile: userProfile) -> userProfile:
        """
        Guarda um novo perfil na base de dados.
        Verifica se já existe um perfil para o user_id antes de inserir.
        As datas de criação e atualização são atribuídas automaticamente pela base de dados.
        Após o insert, o id e as datas reais são lidas da base de dados e atribuídas ao objeto em memória.
        """
        # Verificar se já existe um perfil para este user_id
        existing_profile = self.get_profile_by_user_id(profile.user_id)
        if existing_profile:
            raise ValueError(f"Já existe um perfil para o utilizador com ID {profile.user_id}")
        
        query = """
            INSERT INTO profiles (user_id, nome, data_nascimento, altura_cm, genero, peso_inicial_kg, peso_kg)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            profile.user_id,
            profile.nome,
            profile.data_nascimento,
            profile.altura_cm,
            profile.genero,
            profile.peso_inicial_kg,
            profile.peso_kg
        )
        #insert na base de dados
        self.db.execute(query, params)
        # obter id gerado automaticamente pela base de dados e atualiza o objeto em memória
        profile.id = self.db.cursor.lastrowid

        # obter as datas de criação e atualização atribuídas pela base de dados
        self.db.execute(
            "SELECT data_criacao, ultima_atualizacao FROM profiles WHERE id = %s",
            (profile.id,)
        )
        result = self.db.cursor.fetchone()
        if result:
            profile.data_criacao = result[0]
            profile.ultima_atualizacao = result[1]

        return profile


    def update_profile(self, profile: userProfile) -> userProfile:
        """
        Atualiza um perfil existente na base de dados.
        Preserva a data_criacao original e atualiza apenas ultima_atualizacao.
        """
        if not profile.id:
            raise ValueError("Perfil deve ter ID para ser atualizado")
        
        query = """
            UPDATE profiles 
            SET nome = %s, data_nascimento = %s, altura_cm = %s, genero = %s, 
                peso_inicial_kg = %s, peso_kg = %s
            WHERE id = %s AND user_id = %s
        """
        params = (
            profile.nome,
            profile.data_nascimento,
            profile.altura_cm,
            profile.genero,
            profile.peso_inicial_kg,
            profile.peso_kg,
            profile.id,
            profile.user_id
        )
        
        self.db.execute(query, params)
        
        # Verificar se alguma linha foi afetada
        if self.db.cursor.rowcount == 0:
            raise ValueError("Perfil não encontrado ou não autorizado para atualização")
        
        # Obter a nova data de atualização (atualizada automaticamente pela BD)
        self.db.execute(
            "SELECT ultima_atualizacao FROM profiles WHERE id = %s",
            (profile.id,)
        )
        result = self.db.cursor.fetchone()
        if result:
            profile.ultima_atualizacao = result[0]
        
        return profile

    
    # TODO : TESTES
    def save_or_update_profile(self, profile: userProfile) -> userProfile:
        """
        Método que decide se deve criar ou atualizar o perfil.
        Se o perfil tem ID, atualiza. Se não tem, cria novo.
        """
        if profile.id:
            return self.update_profile(profile)
        else:
            return self.save_new_profile(profile)


    def get_profile_by_user_id(self, user_id: int) -> Optional[userProfile]:
        """
        Retorna um objeto userProfile com base no user_id.
        Retorna None se não existir perfil para o utilizador.
        """
        query = """
            SELECT id, user_id, nome, data_nascimento, altura_cm, genero, peso_inicial_kg, peso_kg, data_criacao, ultima_atualizacao
            FROM profiles WHERE user_id = %s
        """
        self.db.execute(query, (user_id,))
        result = self.db.cursor.fetchone()
        if result:
            return userProfile(
                id=result[0],
                user_id=result[1],
                nome=result[2],
                data_nascimento=result[3],
                altura_cm=result[4],
                genero=result[5],
                peso_inicial_kg=result[6],
                peso_kg=result[7],
                data_criacao=result[8],
                ultima_atualizacao=result[9]
            )
        return None 