from sqlalchemy import insert
import psycopg2
from typing import Tuple, Optional, Dict, Any
from sqlalchemy.engine import Engine as sqlAlchmeyEngine
from psycopg2.extensions import connection as psycopg2Connection


class CpuInfoDao:
    """
    Data Access Object for interacting with the cpu_info table, demonstrating both
    SQLAlchemy Core and psycopg2 methods for database interaction.
    Now with a single public save_cpu_info method and private implementation methods.
    """

    def __init__(self, engine: sqlAlchmeyEngine, psycopg2Conn: psycopg2Connection):
        """
        Initializes CpuInfoDAO with database engine and psycopg2 connection.
        """

        self.engine = engine
        self.psycopg2Conn = psycopg2Conn

    def __saveCpuInfoSqlAlchemy__(self, cpuInfoData: Dict[str, Any]) -> bool:
        """
        (Private) Saves CPU static information using SQLAlchemy Core.
        """

        if not cpuInfoData:
            return False

        try:
            with self.engine.connect() as connection:
                tableName = "cpu_info"
                statement = insert(tableName).values(**cpuInfoData)
                connection.execute(statement)
                connection.commit()

                return True

        except Exception as e:
            print(f"Error saving CPU info (SQLAlchemy Core, DAO - private method): {e}")
            print(e)
            return False

    def __saveCpuInfoPsycopg2__(self, cpuInfoData: Dict[str, Any]) -> bool:
        """
        (Private) Saves CPU static information using raw psycopg2.
        """

        if not cpuInfoData:
            return False

        try:
            cursor = self.psycopg2Conn.cursor()

            query = """
                INSERT INTO cpu_info (model_name, physical_cores, logical_cores, min_frequency_mhz, max_frequency_mhz) 
                VALUES (%s, %s, %s, %s, %s);
                """

            values: Tuple[Any, ...] = (
                cpuInfoData.get("modelName"),
                cpuInfoData.get("physicalCores"),
                cpuInfoData.get("logicalCores"),
                cpuInfoData.get("minFrequencyMhz"),
                cpuInfoData.get("maxFrequencyMhz"),
            )

            cursor.execute(query, values)
            self.psycopg2Conn.commit()
            cursor.close()

            return True

        except Exception as e:
            print(e)
            return False
