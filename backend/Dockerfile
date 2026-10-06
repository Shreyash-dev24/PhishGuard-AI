FROM python:3.11-slim

WORKDIR /app

# Prevent Python from creating .pyc files
# and make logs appear immediately.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required Python packages
RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    pandas \
    numpy \
    scikit-learn \
    joblib \
    tensorflow==2.21.0 \
    sqlalchemy \
    pydantic

# Copy the complete project into the container
COPY . /app

# The application is started from the project root
WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]