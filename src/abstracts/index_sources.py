from abc import ABC, abstractmethod


class IndexFileReader(ABC):
    index_type: str

    @abstractmethod
    def read(self, index_data) -> list[str]:
        pass


class IndexWriter(ABC):
    index_type: str

    @abstractmethod
    def write(self, sources):
        pass


class IndexFileManager(ABC):
    index_type: str

    def __init_subclass__(cls, **kwargs):
        index_type = kwargs.get('index_type')
        if index_type is None:
            raise Exception()
        cls.index_type = index_type

        # set default factories
        for factory_type in ['downloader_factory', 'reader_factory', 'writer_factory']:
            factory = kwargs.get(factory_type)
            if factory is None:
                raise Exception(f"{factory_type}")
            setattr(cls, factory_type, factory)

    def __init__(self, downloader: str = 'default', reader: str = "default", writer: str = "default"):
        self.downloader = self.downloader_factory(downloader)
        self.reader = self.reader_factory(reader)
        self.writer = self.writer_factory(writer)
        self._errors = []
        self._source = None
        self._count = 0

    @abstractmethod
    def run(self, url: str):
        pass

    @property
    def errors(self) -> list[dict]:
        return self._errors

    @property
    def failed(self) -> int:
        return len(self.errors)

    @property
    def successful(self) -> int:
        return self._count - self.failed

    # @property
    # def source(self):
    #   return self._source
