from sqlalchemy_timescaledb.dialect import TimescaledbDDLCompiler  # pip install sqlalchemy-timescaledb
from sqlalchemy import DDL
import random


@staticmethod
def ddl_hypertable(table_name, hypertable):
    time_column_name = hypertable["time_column_name"]
    partitioning_column = hypertable.get("partitioning_column", None)
    number_partitions = hypertable.get("number_partitions")
    chunk_time_interval = hypertable.get("chunk_time_interval", "7 days")

    if isinstance(chunk_time_interval, str):
        if chunk_time_interval.isdigit():
            chunk_time_interval = int(chunk_time_interval)
        else:
            chunk_time_interval = f"INTERVAL '{chunk_time_interval}'"

    return DDL(
        # unique index name 必须唯一，所以加入random打乱，否则报错
        f"CREATE UNIQUE INDEX idx_{str(random.randint(1,99999))}_{partitioning_column}_{time_column_name} ON {table_name}({partitioning_column}, {time_column_name});"
        if partitioning_column
        else ""
        + f"""
        SELECT create_hypertable(
            '{table_name}',
            '{time_column_name}',
            chunk_time_interval => {chunk_time_interval},
            {f"partitioning_column => '{partitioning_column}'," if partitioning_column else ""}
            {f"number_partitions => {number_partitions}," if number_partitions else ""}
            if_not_exists => TRUE
        );
        """
    )


TimescaledbDDLCompiler.ddl_hypertable = ddl_hypertable
