from modelos.planoObjetivo import PlanoObjetivo
from persistencia.basedados.DataBase import DataBase

class PlanoObjetivoRepository:
    def __init__(self, db : DataBase):
        self.db = db


    def save_new_planoObjetivo(self, plano_objetivo : PlanoObjetivo):
        self.db.execute(
            """
            INSERT INTO plano_objetivo (plano_id, objetivo_id, data_inicio, data_fim)
            VALUES (%s, %s, %s, %s)
            """,
            (plano_objetivo.plano_id, plano_objetivo.objetivo_id, plano_objetivo.data_inicio, plano_objetivo.data_fim)
        )

        plano_objetivo.id = self.db.cursor.lastrowid

        return plano_objetivo


    def get_by_plano_id(self, plano_id):
        self.db.execute("SELECT id, plano_id, objetivo_id, data_inicio, data_fim FROM plano_objetivo WHERE plano_id = %s", (plano_id,))
        return [PlanoObjetivo(id=row[0], plano_id=row[1], objetivo_id=row[2], data_inicio=row[3], data_fim=row[4]) for row in self.db.fetchall()] 