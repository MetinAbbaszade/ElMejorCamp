from app import create_app
from uvicorn import run

app = create_app()

run(app=app, host='0.0.0.0', port=8000)