import os

from dotenv import load_dotenv

load_dotenv(override=True)


# Server
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
ENV = os.getenv("ENV", "development")

# Redis URL
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

REDIS_URL = os.getenv(
    "REDIS_URL",
    f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0",
)

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Model
MODEL = os.getenv("MODEL") or os.getenv("CONVERSATION_SERVICE_MODEL")

# Groq settings
USE_GROQ = (
    os.getenv("USE_GROQ") or os.getenv("CONVERSATION_SERVICE_USE_GROQ") or "false"
).lower() == "true"
GROQ_MODEL = os.getenv("GROQ_MODEL") or os.getenv("CONVERSATION_SERVICE_GROQ_MODEL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or os.getenv(
    "CONVERSATION_SERVICE_GROQ_API_KEY"
)


# RabbitMQ URL
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}",
)
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME")

# RabbitMQ Service settings
SERVICE_NAME = os.getenv("SERVICE_NAME", "CONVERSATION_SERVICE")
SERVICE_QUEUE = os.getenv("SERVICE_QUEUE", "CONVERSATION_QUEUE")
RPC_QUEUE = os.getenv("SERVICE_RPC", "CONVERSATION_RPC")

USER_QUEUE = os.getenv("USER_QUEUE")
USER_RPC = os.getenv("USER_RPC")

_imported_variable = {
    "HOST": HOST,
    "PORT": PORT,
    "REDIS_URL": REDIS_URL,
    "JWT_SECRET_KEY": JWT_SECRET_KEY,
    "RABBITMQ_URL": RABBITMQ_URL,
    "EXCHANGE_NAME": EXCHANGE_NAME,
}

if USE_GROQ:
    _imported_variable.update({"GROQ_API_KEY": GROQ_API_KEY, "GROQ_MODEL": GROQ_MODEL})
else:
    _imported_variable.update({"MODEL": MODEL})

if not all(_imported_variable.values()):
    missing_variables = [key for key, value in _imported_variable.items() if not value]
    raise ValueError(f"Missing environment variables: {missing_variables}")


