from app.core import create_app
from app.settings import config
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        reload=config.app.reload, 
        host="0.0.0.0", 
        port=config.app.port
    )