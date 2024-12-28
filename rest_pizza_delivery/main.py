from fastapi import FastAPI
from rest_pizza_delivery.routes.route_auth import auth_router
from rest_pizza_delivery.routes.route_order import order_router
import uvicorn

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)

if __name__ == "__main__":
    uvicorn.run("rest_pizza_delivery.main:app")
