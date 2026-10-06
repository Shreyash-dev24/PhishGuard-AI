from backend.app.db.database import Base, engine
from backend.app.models.prediction_history import PredictionHistory


def init_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")