from rest_pizza_delivery.db.db_config import engine, Base
from db_models import User, Order

# CMD ["sh", "-c", "poetry run uvicorn rest_pizza_delivery.main:app --host 0.0.0.0 --port 8000 --reload"]
Base.metadata.create_all(bind=engine)