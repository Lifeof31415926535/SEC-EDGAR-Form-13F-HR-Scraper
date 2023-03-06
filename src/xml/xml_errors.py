"""Custom Error classes for the XML parser"""


class XMLParserError(Exception):
    pass


class NilEntryError(XMLParserError):
    """Raised whenever an XML table contains a NIL value."""

    def __init__(self, tag: str, message=''):
        self.tag = tag
        self.message = message

        if self.message == '':
            self.message = f"The the entry for tag {self.tag} has a NIL value."

        super().__init__(self.message)

    def __str__(self):
        return f"NilEntryError for tag {self.tag}:  {self.message}."


class EmptyEntryError(XMLParserError):
    """Raised whenever an XML table contains an empty entry."""

    def __init__(self, tag: str, message=''):
        self.tag = tag
        self.message = message

        if self.message == '':
            self.message = f"The the entry for tag {self.tag} was empty."

        super().__init__(self.message)

    def __str__(self):
        return f"NilEntryError for tag {self.tag}:  {self.message}."
