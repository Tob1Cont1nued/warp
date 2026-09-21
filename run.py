"""Entry point: python run.py"""
from dotenv import load_dotenv
load_dotenv()  # liest .env im Projektroot, falls vorhanden (lokal) - auf Render ungenutzt/no-op

from app import app

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
