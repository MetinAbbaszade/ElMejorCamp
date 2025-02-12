from app import create_app
from uvicorn import run

app = create_app()

run(app=app, port=8000)