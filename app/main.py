from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import controller 

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar CORS para permitir peticiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Incluyendo los routers
app.include_router(controller.router, prefix="/automatizacion_CDT", tags=["Revisar las tasas de CDT en distintos bancos"])


"""

Para ejecutar la aplicación, puedes utilizar el siguiente comando:

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

python -m venv venv

source venv/Scripts/activate

pip install pipreqs

pipreqs .


"""