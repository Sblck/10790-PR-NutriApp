## class que associa um  plano com um ou mais objetivos
from datetime import date, datetime

class PlanoObjetivo:
    def __init__(self, plano_id=None, objetivo_id=None, data_inicio=None, data_fim=None, id=None):
        self.id = id
        self.plano_id = plano_id
        self.objetivo_id = objetivo_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def is_active(self, data=None):
        """
        Retorna True se o objetivo está ativo na data dada (ou hoje, se não for especificada).
        """
        if data is None:
            data = date.today()
        elif isinstance(data, str):
            data = datetime.strptime(data, "%Y-%m-%d").date()

        if isinstance(self.data_inicio, str):
            self.data_inicio = datetime.strptime(self.data_inicio, "%Y-%m-%d").date()
        if self.data_fim and isinstance(self.data_fim, str):
            self.data_fim = datetime.strptime(self.data_fim, "%Y-%m-%d").date()
        return self.data_inicio <= data and (self.data_fim is None or self.data_fim >= data)

    def __repr__(self):
        return f"<PlanoObjetivo id={self.id} plano_id={self.plano_id} objetivo_id={self.objetivo_id} data_inicio={self.data_inicio} data_fim={self.data_fim}>" 