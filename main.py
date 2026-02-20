from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Detail(BaseModel):
    ProductId: int
    QtyDus: int
    QtyPcs: int


class Penerimaan(BaseModel):
    TrxInNo: str
    WhsIdf: int
    TrxInDate: date
    TrxInSuppIdf: int
    TrxInNotes: str
    details: List[Detail]

class Pengeluaran(BaseModel):
    TrxOutNo: str
    WhsIdf: int
    TrxOutDate: date
    TrxOutCustIdf: int
    TrxOutNotes: str
    details: List[Detail]

data_penerimaan = []
data_pengeluaran = []

@app.get("/")
def root():
    return {"message": "Backend berjalan"}

@app.post("/penerimaan")
def create_penerimaan(data: Penerimaan):
    data_penerimaan.append(data)
    return {"message": "Data penerimaan berhasil disimpan"}


@app.get("/penerimaan")
def get_penerimaan():
    return data_penerimaan

@app.post("/pengeluaran")
def create_pengeluaran(data: Pengeluaran):
    data_pengeluaran.append(data)
    return {"message": "Data pengeluaran berhasil disimpan"}

@app.get("/pengeluaran")
def get_pengeluaran():
    return data_pengeluaran

@app.get("/stok")
def get_stok():
    stok = {}

    for trx in data_penerimaan:
        for d in trx.details:
            if d.ProductId not in stok:
                stok[d.ProductId] = {"QtyDus": 0, "QtyPcs": 0}

            stok[d.ProductId]["QtyDus"] += d.QtyDus
            stok[d.ProductId]["QtyPcs"] += d.QtyPcs

    for trx in data_pengeluaran:
        for d in trx.details:
            if d.ProductId not in stok:
                stok[d.ProductId] = {"QtyDus": 0, "QtyPcs": 0}

            stok[d.ProductId]["QtyDus"] -= d.QtyDus
            stok[d.ProductId]["QtyPcs"] -= d.QtyPcs

    return stok