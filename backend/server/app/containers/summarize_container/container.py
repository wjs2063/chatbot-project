from dependency_injector import containers, providers
from services.summarize_service import SummarizeService, ChatGPT, AudioHandler, STTHandler


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    summarize_service = providers.Singleton(
        SummarizeService,
        chatgpt=providers.Singleton(ChatGPT),
        audiohandler=providers.Singleton(AudioHandler),
        stthandler=providers.Singleton(STTHandler)
    )
