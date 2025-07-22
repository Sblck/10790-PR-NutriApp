# Plano -  um plano contem um ou mais objetivos

class Plano:
    def __init__(self, nome, estado,
        id = None, 
        user_id = None,
        data_inicio = None,
        data_fim = None,
        objetivos = None
        ):
            self.id = id
            self.user_id = user_id
            self.nome = nome
            self.data_inicio = data_inicio
            self.data_fim = data_fim
            self.estado = estado
            #lista de objetos tipo PlanoObjetivo em run-time
            self.objetivos = objetivos or []  


    def is_active(self):
        """Retorna True se o plano está ativo (sem data_fim ou estado == 'ativo')."""
        return self.estado == 'ativo' and self.data_fim is None


    def is_valid(self):
        """Valida se os campos obrigatórios estão preenchidos."""
        return all([
            self.user_id is not None,
            self.nome is not None,
            self.data_inicio is not None,
            self.estado is not None
        ])
    

    def add_objetivo(self, plano_objetivo):
        """
        Adiciona à lista de objetivos corrente um objetivo (PlanoObjetivo)
        """
        self.objetivos.append(plano_objetivo)


# toString() equivalente de java
    def __repr__(self):
        return f"<Plan id={self.id} nome={self.nome} user_id={self.user_id} estado={self.estado}>"


    