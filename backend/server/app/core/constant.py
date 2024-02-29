from core.config import settings

AUDIO_BASE_PATH = "/code/backend/server"

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTE = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)


