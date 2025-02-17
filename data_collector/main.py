import configparser
from database.database_connection import connect_db
import os
from typing import Tuple
from psycopg2.extensions import connection as psycopg2Connection
from sqlalchemy.engine import Engine as sqlAlchemyEngine
from system_metrics.cpu_info_service import CpuInfoService


def connectDatabase() -> Tuple[psycopg2Connection, sqlAlchemyEngine]:
    config = configparser.ConfigParser()

    # Construct full path to config.ini relative to main.py's directory
    currentDir = os.path.dirname(
        os.path.abspath(__file__)
    )  # Get directory of current script (main.py)

    configFilePath = os.path.join(
        currentDir, "config.ini"
    )  # config.ini is in the same directory as main.py

    config.read(configFilePath)

    conn_psycopg2, engine_sqlalchemy = connect_db(config)  # Get both connections
    if (
        not conn_psycopg2 or not engine_sqlalchemy
    ):  # Check if both connections are successful
        print(
            "Database connection failed in main.py (psycopg2 or SQLAlchemy). Exiting."
        )
        return

    print("Database connections (psycopg2 and SQLAlchemy) successful in main.py.")

    return conn_psycopg2, engine_sqlalchemy


def saveCpuStaticInfo(cpuInfo: CpuInfoService) -> bool:
    """Saves CPU static information using the provided service."""
    return cpuInfo.saveCpuInfo(False)


def main():
    conn_psycopg2, engine_sqlalchemy = connectDatabase()

    cpu_info_service = CpuInfoService(engine_sqlalchemy, conn_psycopg2)
    cpuStaticInfo = saveCpuStaticInfo(cpu_info_service)

    print(cpuStaticInfo)


if __name__ == "__main__":
    main()
