from core.config import settings

audio_base_path = "audio_dir"

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTE = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)


