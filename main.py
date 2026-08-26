from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import random
import asyncio
import time

# Inisialisasi Aplikasi (Otomatis membuat UI dokumentasi untuk HR)
app = FastAPI(
    title="Intrinsic Edge-AI Chaos Proxy",
    description="Demo Chaos Engineering: Menguji ketahanan API terhadap Latensi, Timeout, dan Malformed Input.",
    version="1.0.0"
)

# Status Chaos Mode (Global State sederhana)
chaos_state = {
    "is_active": False,
    "latency_chance": 0.5, # 50% kemungkinan delay
    "error_chance": 0.3    # 30% kemungkinan HTTP 503
}

# --- CHAOS MIDDLEWARE ---
@app.middleware("http")
async def chaos_middleware(request: Request, call_next):
    # Hanya serang endpoint /predict
    if chaos_state["is_active"] and "/predict" in request.url.path:
        
        # 1. Injeksi Latency / AI Timeout (2 - 5 detik)
        if random.random() < chaos_state["latency_chance"]:
            delay = random.uniform(2.0, 5.0)
            await asyncio.sleep(delay)
            
        # 2. Injeksi Service Interruption / Node Mati
        if random.random() < chaos_state["error_chance"]:
            return JSONResponse(
                status_code=503, 
                content={"error": "Chaos Injected: Service Unavailable. AI Node Offline."}
            )

    # Lanjutkan request jika aman
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    return response

# --- SCHEMAS ---
class SensorData(BaseModel):
    robot_id: str
    sensor_reading: float
    timestamp: str

# --- ENDPOINTS ---
@app.get("/", tags=["General"])
def read_root():
    return {"message": "Welcome HR/Engineering Team. Please visit /docs to test the Chaos API interactively."}

@app.post("/admin/toggle-chaos", tags=["Chaos Control"])
def toggle_chaos(active: bool):
    """Gunakan ini untuk menyalakan atau mematikan Chaos Mode"""
    chaos_state["is_active"] = active
    return {"message": f"Chaos mode is now {'ACTIVE' if active else 'INACTIVE'}"}

@app.post("/predict", tags=["AI Engine"])
def predict_action(data: SensorData):
    """Simulasi endpoint AI Inference. Coba kirim malformed data (Fuzzing) ke sini."""
    # Logika simulasi AI sederhana
    if data.sensor_reading > 100:
        action = "EMERGENCY_STOP"
    else:
        action = "CONTINUE"
        
    return {
        "robot_id": data.robot_id,
        "predicted_action": action,
        "status": "Success"
    }
