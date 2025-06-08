import uvicorn
from fastapi import FastAPI
from routers import router
from setting import settings

app = FastAPI(title="Реализация REST API для работы с пользователями", version="0.0.1")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )
