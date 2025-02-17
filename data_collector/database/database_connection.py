import psycopg2
import configparser
from sqlalchemy import create_engine, text  # Import SQLAlchemy components
from typing import Tuple, Optional  # Import Tuple and Optional for type hinting
from psycopg2.extensions import connection as Psycopg2Connection
from sqlalchemy.engine import Engine as SQLAlchemyEngine


def connect_db(
    config: configparser.ConfigParser,
) -> Tuple[Optional[Psycopg2Connection], Optional[SQLAlchemyEngine]]:
    """
    Establishes a connection to the PostgreSQL database using psycopg2
    and creates an SQLAlchemy Engine.

    Args:
        config (configparser.ConfigParser): Parsed configuration object.

    Returns:
        tuple: A tuple containing:
            - psycopg2.extensions.connection: Database connection object (psycopg2) if successful, None otherwise.
            - sqlalchemy.engine.Engine: SQLAlchemy Engine object if successful, None otherwise.
    """

    dbConfig = config["database"]

    try:
        # connect using psycopg2
        connPsycopg2 = psycopg2.connect(
            host=dbConfig.get("host"),
            dbname=dbConfig.get("dbname"),
            user=dbConfig.get("user"),
            password=dbConfig.get("password"),
            port=dbConfig.get("port"),
        )
        print("psycopg2 connection established successfully from database.py.")

        # Create SQLAlchemy Engine (using the same connection parameters)
        sqlAlchemyEngine = create_engine(
            f"postgresql+psycopg2://{dbConfig.get('user')}:{dbConfig.get('password')}@{dbConfig.get('host')}:{dbConfig.get('port') or 5432}/{dbConfig.get('dbname')}",
            echo=False,
        )  # echo=True for debugging SQL)

        print("SQLAlchemy Engine created successfully from database.py.")

        return connPsycopg2, sqlAlchemyEngine

    except psycopg2.Error as e:
        print(f"Database connection error from database.py: {e}")
        return None, None  # Return None for both if connection fails
