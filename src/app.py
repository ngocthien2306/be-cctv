import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.utils.socket import socket_connection
from src.utils.project_config import project_config
from src.router.docs_router import add_docs_router
from src.router import event_router
from src.router import history_router
from src.router import report_router


app = FastAPI(
    version=1.0,
    title=project_config.DOCS_TITLE,
    debug=project_config.DEBUG, 
    docs_url=None, 
    redoc_url=None
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/ws", socket_connection())
app.mount("/public", StaticFiles(directory="/home/i-soft/volume_container_cuda-11.2"), name="public")


add_docs_router(app)
app.include_router(event_router.router)
app.include_router(history_router.router)
app.include_router(report_router.router)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=project_config.BE_PORT)
