import pandas as pd
import civis

MAGIC_NAME = 'civisquery'


def magic(line, cell=None):
    """Civis query magic.

    This magic works both as a cell magic (for table previews) and a
    line magic to query a table and return a DataFrame.
    """

    client = civis.APIClient()

    if cell is None:
        # Not using maxsplit kwarg b/c it is not compatible w/ Python 2
        database, sql = line.split(' ', 1)
        df = civis.io.read_civis_sql(
            sql, database.strip(), use_pandas=True, client=client)
        if len(df) == 0:
            df = None
    else:
        database = line.strip()
        sql = cell

        fut = civis.io.query_civis(
            sql, database, client=client, preview_rows=100)
        res = fut.result()
        if len(res['result_rows']) > 0:
            df = pd.DataFrame.from_records(
                res['result_rows'], columns=res['result_columns'])
        else:
            df = None

    return df
