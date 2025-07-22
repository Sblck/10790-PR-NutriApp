from persistencia.repositorios.PlanoRepository import PlanoRepository

class PlanoService:
    def __init__(self, plano_repo: PlanoRepository):
        self.plano_repo = plano_repo

    def get_plano_ativo(self, user_id):
        """
        Devolve o plano ativo do utilizador (estado='ativo').
        Retorna None se não existir.
        """
        planos = self.plano_repo.get_by_user_id(user_id)
        for plano in planos:
            if plano.estado == 'ativo':
                return plano
        return None 