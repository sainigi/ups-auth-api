import logging
from typing import Dict, List
from app.commons.db_helper import getCursor, getCursorSync

logger = logging.getLogger()

async def exec_stored_procedure(sp_name: str, param_names: List, param_values: List, fetch_data: bool= True):
    try:
        stored_proc = f"EXEC [MKSIdentity].[{sp_name}] {', '.join([f'@{name} = ?' for name in param_names])}"
        params = tuple(param_values)
        cursor, conn = await getCursor()
        cursor.execute(stored_proc, params)
        data = None
        if fetch_data:
            data = cursor.fetchall()
        conn.commit()
        conn.close()
        logger.debug(f'Successfully executed {sp_name} Stored Procedure...')
        return data

    except Exception as ex:
        raise
def exec_stored_procedure_sync(sp_name: str, param_names: List, param_values: List, fetch_data: bool= True):
    try:
        stored_proc = f"EXEC [{sp_name}] {', '.join([f'@{name} = ?' for name in param_names])}"
        params = tuple(param_values)
        cursor, conn = getCursorSync()
        cursor.execute(stored_proc, params)
        data = None
        if fetch_data:
            data = cursor.fetchall()
        conn.commit()
        conn.close()
        logger.debug(f'Successfully executed {sp_name} Stored Procedure...')
        return data

    except Exception as ex:
        raise
    
async def exec_stored_procedure_multiple_sets(sp_name: str, param_names: List, param_values: List, fetch_data: bool= True):
    try:
        stored_proc = f"EXEC [MKSIdentity].[{sp_name}] {', '.join([f'@{name} = ?' for name in param_names])}"
        params = tuple(param_values)
        cursor, conn = await getCursor()
        cursor.execute(stored_proc, params)
        data = []
        if fetch_data:
            while True:
                rows = cursor.fetchall()
                data.append(rows)
                if not cursor.nextset():
                    break

        conn.commit()
        conn.close()
        return data

    except Exception as ex:
        raise