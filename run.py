"""Entry point: python run.py"""
from dotenv import load_dotenv
load_dotenv()  # liest .env im Projektroot, falls vorhanden (lokal) - auf Render ungenutzt/no-op

from app import app

if __name__ == "__main__":
    # threaded=True: die Play-Buttons der Testdokumentation (/admin/tests/run)
    # blockieren sonst diesen einzigen Request-Thread, während Playwright-Tests
    # denselben Server unter 127.0.0.1:5000 aufrufen müssen (siehe live_server-Fixture).
    app.run(debug=True, host="127.0.0.1", port=5000, threaded=True)
