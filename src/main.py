# ruff: noqa: E402
import logging
import sys
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

# позволяет определить путь текущего файла, его родителя src, и родителя src
sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.init_cache import redis_manager
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    logging.info(" Initialized FastAPI cache")
    yield
    await redis_manager.close()
    # при завершении/перезагрузке приложения


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,  # type: ignore
        title=app.title + " - Swagger UI",  # type: ignore
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,  # type: ignore
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)