from fastapi import FastAPI

from app.api.v1 import user_route
from app.api.v1 import inventory_route
from app.api.v1 import product_route, order_route
from app.api.v1 import auth

app = FastAPI(docs_url="/docs", redoc_url="/redoc", openapi_url="/openapi.json")


app.include_router(router=product_route.router)
app.include_router(router=order_route.router)
app.include_router(router=inventory_route.inventory_router)
app.include_router(router=auth.auth_router)
app.include_router(router=user_route.user_router)
