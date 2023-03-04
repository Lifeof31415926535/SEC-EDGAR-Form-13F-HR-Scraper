from forms_index_files import FormsIndexFileManager


class IndexFileManagerFactory:
    def __call__(self, index_type: str = 'default', settings: dict = None):
        settings = {} if settings is None else settings
        match index_type:
            case 'default' | 'Default' | 'forms' | 'Forms':
                return FormsIndexFileManager(**settings)
            case _:
                raise Exception()
