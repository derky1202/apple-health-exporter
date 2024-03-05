import os
import dotenv
import uuid
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, parse_obj_as
from sqlalchemy import JSON, UUID, Column, DateTime, String, create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import declarative_base, sessionmaker
import uvicorn
import json
import db #db.py也要看一下

app = FastAPI()
dotenv.load_dotenv()
DATABASE_URL = os.environ.get(
    "postgres", "timescaledb://postgres:postgres@apple-health-db:5432/postgres"
)  # 这里运行换成DB_2, docker 则是 DATABASE_URL
DATABASE_URL = DATABASE_URL.replace("postgresql://", "timescaledb://")
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class MetricTable_LIN(Base):
    __tablename__ = "apple_metrics_lin"
    id = Column(UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String)
    data = Column(JSON)
    timestamp = Column(DateTime())
    # Add index
    __table_args__ = {
        "timescaledb_hypertable": {
            "time_column_name": "timestamp",
            "partitioning_column": "name",
            "number_partitions": 10,
        }
    }


class MetricTable_DP(Base):
    __tablename__ = "apple_metrics_dp"
    id = Column(UUID, default=uuid.uuid4, primary_key=True)
    name = Column(String)
    data = Column(JSON)
    timestamp = Column(DateTime())
    # Add index
    __table_args__ = {
        "timescaledb_hypertable": {
            "time_column_name": "timestamp",
            "partitioning_column": "name",
            "number_partitions": 10,
        }
    }


Base.metadata.create_all(engine)


class Datum(BaseModel):
    date: str
    source: Optional[str] = None
    qty: Optional[float] = None
    avg: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    deep: Optional[float] = None
    core: Optional[float] = None
    awake: Optional[float] = None
    asleep: Optional[float] = None
    sleep_end: Optional[str] = None
    in_bed_start: Optional[str] = None
    in_bed_end: Optional[str] = None
    sleep_start: Optional[str] = None
    rem: Optional[float] = None
    in_bed: Optional[float] = None


class Metric(BaseModel):
    units: str
    data: List[Datum]
    name: str


class Data(BaseModel):
    metrics: List[Metric]


class RequestData(BaseModel):
    data: Data


# 必须以这种格式才能curl成功
# curl -X POST "http://192.168.2.21:38000/upload/lin" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@/Users/lin/Downloads/HealthAutoExport-2023-07-01-2023-07-08.json"

@app.post("/upload/{usr}") # 对应下面的 usr: str 不写就报错
async def upload_data(usr: str, file: UploadFile = File(...)):
    content = await file.read()
    request_data = parse_obj_as(RequestData, json.loads(content.decode("utf-8")))
    ps = []

    for metric in request_data.data.metrics:
        for datum in metric.data:
            data = datum.model_dump()
            date = data.pop("date", None)
            ps.append(dict(name=metric.name, data=data, timestamp=date))
    with SessionLocal() as session:
        if usr == "lin":
            insert_ps = insert(MetricTable_LIN).values(ps).on_conflict_do_nothing(index_elements=["name", "timestamp"])
        elif usr == "dp":
            insert_ps = insert(MetricTable_DP).values(ps).on_conflict_do_nothing(index_elements=["name", "timestamp"])
        session.execute(insert_ps)
        session.commit()
    return {"status": "Data uploaded successfully!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=38001)
