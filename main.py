from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import random
import asyncio
import time

# --- APP INITIALIZATION ---
app = FastAPI(
    title="Intrinsic Edge-AI Chaos Proxy",
    description="A resilience engineering middleware designed to proactively identify potential problems within APIs, SDKs, and cloud-to-edge communication layers through automated fault injection.",
    version="1.1.0"
)

# --- GLOBAL CHAOS STATE ---
chaos_state = {
    "is_active": False,
    "latency_chance": 0.5, # 50% chance to inject delay
    "error_chance": 0.3    # 30% chance to drop request (HTTP 503)
}

# --- CHAOS MIDDLEWARE ---
@app.middleware("http")
async def chaos_middleware(request: Request, call_next):
    # Only target the AI prediction endpoint to simulate edge inference issues
    if chaos_state["is_active"] and "/predict" in request.url.path:
        
        # 1. Inject Latency / AI Timeout (1 - 3 seconds for Serverless limits)
        if random.random() < chaos_state["latency_chance"]:
            delay = random.uniform(1.0, 3.0)
            await asyncio.sleep(delay)
            
        # 2. Inject Service Interruption / Edge Node Offline
        if random.random() < chaos_state["error_chance"]:
            return JSONResponse(
                status_code=503, 
                content={"error": "Chaos Injected: Service Unavailable. Edge Node Offline or Unreachable."}
            )

    # Proceed with the request safely if no chaos was injected
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    return response

# --- DATA SCHEMAS ---
class SensorData(BaseModel):
    robot_id: str
    sensor_reading: float
    timestamp: str

# --- ENDPOINTS ---

@app.get("/", tags=["General"])
def read_root():
    return {
        "message": "Welcome to the Edge-AI Chaos Proxy Demo.",
        "action": "Please navigate to /docs to interact with the API and test the resilience features."
    }

@app.post("/admin/toggle-chaos", tags=["Chaos Control"])
def toggle_chaos(active: bool):
    """
    Toggle the chaos mode on or off.
    When active, the proxy will randomly inject network latency and service disruptions.
    """
    chaos_state["is_active"] = active
    return {"message": f"Chaos mode is now {'ACTIVE' if active else 'INACTIVE'}"}

@app.get("/system/proactive-probe", tags=["Proactive Monitoring"])
def proactive_system_probe():
    """
    Simulates a monitoring system that proactively identifies potential problems 
    within our APIs, SDKs, web interfaces, and cloud-to-edge communication layers.
    """
    # 1. Check Internal API Layer
    api_status = "Healthy"
    
    # 2. Check Cloud-to-Edge Communication Layer (Simulating connection to remote robots)
    edge_communication = "Stable"
    
    # Proactive Detection: If chaos (anomalies) are active in the network
    if chaos_state["is_active"]:
        if chaos_state["error_chance"] > 0:
            edge_communication = "WARNING: Packet loss and node disconnections detected in Cloud-to-Edge telemetry."
        elif chaos_state["latency_chance"] > 0:
            edge_communication = "WARNING: High network latency detected across industrial edge nodes."

    # 3. Check Web Interfaces & SDK Gateways
    sdk_web_gateway = "Operational"

    # Evaluate Overall Platform Endurance & Stability
    is_degraded = "WARNING" in edge_communication
    overall_health = "Degraded (At Risk)" if is_degraded else "Optimal"

    return {
        "timestamp": time.time(),
        "platform_endurance_status": overall_health,
        "layers_probed": {
            "apis_and_internal_services": api_status,
            "cloud_to_edge_communication": edge_communication,
            "sdks_and_web_interfaces": sdk_web_gateway
        },
        "proactive_action_taken": "Triggered automated failover routing and degraded-mode operation." if is_degraded else "None required"
    }

@app.post("/predict", tags=["AI Engine"])
def predict_action(data: SensorData):
    """
    Mock endpoint for an AI Inference Engine on an edge device. 
    Use this to test payload fuzzing (malformed inputs) and latency resilience.
    """
    # Simple simulation logic for robotics decision making
    if data.sensor_reading > 100.0:
        action = "EMERGENCY_STOP"
    else:
        action = "CONTINUE_OPERATION"
        
    return {
        "robot_id": data.robot_id,
        "predicted_action": action,
        "status": "Success"
    }
