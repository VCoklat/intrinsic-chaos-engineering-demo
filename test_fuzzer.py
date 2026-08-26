from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fuzzing_malformed_payload():
    """Mengirim data yang rusak (string pada field float, missing fields)."""
    bad_payload = {
        "robot_id": "RBT-99",
        "sensor_reading": "bukan_angka", # Sengaja disalahkan
        # timestamp sengaja dihilangkan
    }
    
    response = client.post("/predict", json=bad_payload)
    
    # Harapan: Sistem tidak crash (Error 500), tapi menolak dengan aman (Error 422 Unprocessable Entity) -> Graceful Degradation
    assert response.status_code == 422
    print("Fuzzing Test Passed: System handled malformed input gracefully.")
