import psutil
from typing import Dict, Any, Optional
from sqlalchemy import engine as sqlAlchemyEngine
from psycopg2.extensions import connection as psycopg2Connection
from platform import processor
from database.cpu_info_dao import CpuInfoDao


class CpuInfoService:
    """
    Service layer for collecting and saving CPU static information.
    Uses private methods for internal operations and a public method for saving data.
    """

    def __init__(self, engine: sqlAlchemyEngine, psycopg2Conn: psycopg2Connection):
        """
        Initializes CPUInfoService with database connections and DAO.
        """

        self.cpuInfoDao = CpuInfoDao(engine, psycopg2Conn)

    def _getCpuStaticInfo__(
        self,
    ) -> Optional[Dict[str, Any]]:
        """
        (Private) Collects static CPU information using psutil.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing CPU information, or None if an error occurs.
        """

        try:
            cpuInfoData: Dict[str, Any] = {
                "modelName": "AMD Ryzen 5 7600",
                "physicalCores": psutil.cpu_count(logical=False),
                "logicalCores": psutil.cpu_count(),
                "minFrequencyMhz": psutil.cpu_freq().max,
                "maxFrequencyMhz": "5100.0",
            }

            return cpuInfoData

        except Exception as e:
            print(e)
            return None

    def saveCpuInfo(self, useSqlAlchemy: Optional[bool] = True) -> bool:
        """
        (Public) Orchestrates saving CPU static information, collecting data internally.

        Args:
            use_sqlalchemy (bool, optional): True to use SQLAlchemy, False for psycopg2. Defaults to True.

        Returns:
            bool: True if saving was successful, False otherwise.
        """

        cpuInfoData = self._getCpuStaticInfo__()

        if useSqlAlchemy:
            self.cpuInfoDao.__saveCpuInfoSqlAlchemy__(cpuInfoData)
        else:
            self.cpuInfoDao.__saveCpuInfoPsycopg2__(cpuInfoData)
