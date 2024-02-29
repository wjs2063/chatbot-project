from dependency_injector import containers, providers
from services.stream_service import StreamService
from components.stream import DownloadService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])
    stream_service = providers.Singleton(StreamService)
    download_service = providers.Singleton(DownloadService)