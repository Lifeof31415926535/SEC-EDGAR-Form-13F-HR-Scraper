from abstracts import SourceReader
from forms_index_files import FormsIndexFileManager
from form_index_source_readers import PostgresFormSourceReader


class IndexFileManagerFactory:
    def __call__(self, index_type: str = 'default', settings: dict = None):
        settings = {} if settings is None else settings
        match index_type:
            case 'default' | 'Default' | 'forms' | 'Forms':
                return FormsIndexFileManager(**settings)
            case _:
                raise Exception('')


class IndexSourceReaderFactory:
    def __call__(self, reader_type: str, batch_size=20, **kwargs) -> SourceReader:
        match reader_type:
            case 'default' | 'Default' | 'form-postgres':
                return PostgresFormSourceReader(batch_size=batch_size, **kwargs)
            case _:
                raise Exception('')
