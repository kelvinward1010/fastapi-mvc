import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from .core.config import settings
from .db import init_db
from .routes import auth



app = FastAPI(title=settings.APP_TITLE, root_path=settings.ROOT_PATH)

origins = ['*', 'https://www.google.com']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Welcome to API Server"], response_class=HTMLResponse)
def welcome():
    return """
        <html>
            <head>
                <title>FastAPI-MongoDB</title>
            </head>
            <body>
                <h1>Learn everything in the world!</h1>
            </body>
        </html>
    """
    
app.add_event_handler("startup", init_db.connect_db)
app.add_event_handler("shutdown", init_db.close_db)

app.include_router(auth.router)    

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)