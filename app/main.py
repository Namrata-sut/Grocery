from fastapi import FastAPI
from app.api.v1 import inventory_route
from app.api.v1 import product_route, order_route

app = FastAPI()

app.include_router(router=product_route.router)
app.include_router(router=order_route.router)
app.include_router(router=inventory_route.inventory_router)
