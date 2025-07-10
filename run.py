from app import create_app
from asgiref.wsgi import WsgiToAsgi
import uvicorn

# Create the Flask app
flask_app = create_app()

# Convert Flask (WSGI) to ASGI
asgi_app = WsgiToAsgi(flask_app)

# Run with Uvicorn
if __name__ == "__main__":
    uvicorn.run(asgi_app, host="127.0.0.1", port=8000)
