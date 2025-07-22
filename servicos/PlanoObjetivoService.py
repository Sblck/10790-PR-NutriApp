from persistencia.repositorios.PlanoObjetivoRepository import PlanoObjetivoRepository
from persistencia.repositorios.ObjetivoRepository import ObjetivoRepository

class PlanoObjetivoService:
    def __init__(self, plano_objetivo_repo: PlanoObjetivoRepository, objetivo_repo: ObjetivoRepository):
        self.plano_objetivo_repo = plano_objetivo_repo
        self.objetivo_repo = objetivo_repo

    def get_objetivo_ativo(self, plano_id, data=None):
        """
        Devolve o objetivo ativo para o plano na data dada.
        Retorna None se não existir.
        """
        objetivos = self.plano_objetivo_repo.get_by_plano_id(plano_id)
        for plano_obj in objetivos:
            if plano_obj.is_active(data):
                # get o nome do objetivo
                objetivo = self.objetivo_repo.get_by_id(plano_obj.objetivo_id)
                plano_obj.nome = objetivo.nome if objetivo else None
                return plano_obj
        return None 