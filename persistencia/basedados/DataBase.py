import configparser
from typing import Mapping
import mysql.connector


class DataBase:
    """
    Classe responsável por gerir a ligação a base de dados e fornecer métodos utilitários
    para executar comandos SQL, obter resultados e criar as tabelas principais do sistema.
    Lê as configurações do ficheiro config.ini.
    """
    def __init__(self, config_path='config.ini'):
        """
        Inicializa o objeto DataBase, carregando as configurações do ficheiro config.ini.
        Nota : Não estabelece ligação nem cria a base de dados automaticamente.
        """
        self.config = self.load_config(config_path)
        self.connection = None
        self.cursor = None


    def load_config(self, config_path : str) -> Mapping[str, str]: 
        """
        Lê e retorna as configurações do ficheiro config.ini. (Mapa)
        """
        config = configparser.ConfigParser()
        read_files = config.read(config_path)
        if not read_files:
            raise FileNotFoundError(f"Ficheiro de configuração '{config_path}' não encontrado.")
        if 'database' not in config:
            raise KeyError("Secção [database] em falta no ficheiro de configuração.")
        db = config['database']
        required_keys = ['host', 'user', 'password', 'dbname']
        for key in required_keys:
            if key not in db:
                raise KeyError(f"Chave '{key}' em falta na secção [database] do config.ini.")
        return db


    def connect(self, with_db: bool = True) -> mysql.connector.connection.MySQLConnection:
        """
        Cria e retorna uma ligação MySQL ao servidor, com ou sem especificar a base de dados.

        :param with_db: Se True, conecta diretamente à base de dados especificada nas configurações.
                        Se False, conecta apenas ao servidor (usado para criar a base de dados).
        :return: Instância de MySQLConnection estabelecida.
        """
        db = self.config
        params = {
            'host': db['host'],
            'user': db['user'],
            'password': db['password']
        }
        if with_db:
            params['database'] = db['dbname']
        return mysql.connector.connect(**params)
    


    def create_database_if_not_exists(self):
        """
        Conecta ao MySQL sem especificar a base de dados e cria a base de dados se não existir.
        """
        try:
            conn = self.connect(with_db=False)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['dbname']}")
            cursor.close()
            conn.close()
        except mysql.connector.Error as erro:
            print("Erro ao criar/verificar a base de dados:", erro)
            raise


    def connect_to_data_base(self):
        """
        Estabelece ligação à base de dados especificada nas configurações.
        """
        try:
            self.connection = self.connect(with_db=True)
            self.cursor = self.connection.cursor()
            print("Ligação estabelecida com sucesso!")
        except mysql.connector.Error as erro:
            print("Erro ao conectar à base de dados:", erro)
            raise


    def execute(self, query, params=None):
        """
        Executa um comando SQL (INSERT, UPDATE, DELETE, etc.) na base de dados.
        :param query: Comando SQL a ser executado.
        :param params: Parâmetros opcionais para o comando SQL.
        """
        self.cursor.execute(query, params or ())
        # !! nao fazer commits a selects --> bug !!
        if not query.strip().lower().startswith("select"):
            self.connection.commit()


    def fetchall(self):
        """
        Retorna todos os resultados da última consulta executada.
        :return: Lista de tuplos com os resultados.
        """
        return self.cursor.fetchall()


    def create_tables(self):
        """
        Cria as tabelas principais do sistema, se não existirem.
        """
        # TODO :  SEPARAR POR ENTIDADE
        self.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                nome VARCHAR(255),
                data_nascimento DATE,
                altura_cm INT,
                genero CHAR(1),
                peso_inicial_kg DECIMAL(5,2),
                peso_kg DECIMAL(5,2),
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                ultima_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        # outras


    def close(self):
        """
        Fecha o cursor e a ligação com a base de dados.
        NOTA : Deve ser chamado ao terminar as operações com a base de dados.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()