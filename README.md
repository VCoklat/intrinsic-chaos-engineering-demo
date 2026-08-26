Edge-AI Chaos Proxy & Resilience Fuzzer

Ever wondered how your industrial robotics or edge deployment would handle a wonky network or messed-up sensor data? This project intentionally messes with the API to make sure the system doesn't crash and burn when things go sideways. Built with Python and FastAPI, it's a lightweight middleware proxy and fuzzer that puts your robotics software to the test.

Try it Live

No need to clone the repo – the API is live with an interactive Swagger UI. Check it out: https://intrinsic-chaos-engineering-demo.vercel.app/docs

How to Test

    Check the system's health: GET /system/proactive-probe
    Flip the chaos switch: POST /admin/toggle-chaos → set to true
    Watch the chaos unfold: GET /system/proactive-probe again
    Test the AI engine: POST /predict a few times


What it Does

    Adds random delays to simulate slow networks or AI timeouts
    Drops requests to mimic an offline edge node
    Monitors internal APIs and cloud-to-edge communication
    Throws malformed data at the API to test error handling
    Automated tests run on every GitHub push


Run it Locally

    Clone the repo: git clone https://github.com/yourusername/intrinsic-chaos-engineering-demo.git
    Set up a virtual environment (optional but recommended)
    Install dependencies: pip install -r requirements.txt
