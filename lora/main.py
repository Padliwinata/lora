from typing import List
import datetime

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel


class Record(BaseModel):
    date: datetime.date
    time: datetime.time
    voltage: float
    current: float
    battery: int


app = FastAPI()


@app.get('/get_data')
def get_data() -> List[Record]:
    data = pd.read_csv('data.txt')
    records = []
    for _, row in data.iterrows():
        record = Record(
            date=row['date'],
            time=row['time'],
            voltage=row['voltage'],
            current=row['current'],
            battery=row['battery']
        )
        records.append(record)
    return records

