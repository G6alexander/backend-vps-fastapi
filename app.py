from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from supabase_client import supabase
from typing import Optional

app = FastAPI(title="Chinook Invoice Backend")

class InvoiceHeader(BaseModel):
    invoice_id: int
    customer_id: int
    invoice_date: str
    billing_address: Optional[str] = None
    billing_city: Optional[str] = None
    billing_state: Optional[str] = None
    billing_country: Optional[str] = None
    billing_postal_code: Optional[str] = None
    total: float

@app.get("/health")
def health():
    """Endpoint de health check para el monitor del frontend."""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/invoice")
def create_invoice(header: InvoiceHeader):
    """Graba la cabecera de la factura en Supabase."""
    try:
        print("DATOS RECIBIDOS DE JAVA:", header)
        data = header.dict()
        response = supabase.table("invoice").insert(data).execute()
        if not response.data:
            raise HTTPException(status_code=500, detail="No se pudo insertar en Supabase")
        return {"status": "ok", "data": response.data}
    except Exception as e:
        print("ERROR EN FASTAPI:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/invoice/bulk")
def create_invoices_bulk(headers: list[InvoiceHeader]):
    """Sincronización masiva de cabeceras pendientes."""
    try:
        data = [h.dict() for h in headers]
        response = supabase.table("invoice").insert(data).execute()
        return {"status": "ok", "inserted": len(response.data)}
    except Exception as e:
        print("ERROR EN BULK FASTAPI:", str(e))
        raise HTTPException(status_code=500, detail=str(e))