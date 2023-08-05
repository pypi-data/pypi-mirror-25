from django_asservio_core.models import (
    CodeDictionary, NameDictionary,
    Dictionary, DescriptionDictionary
)


class Code(CodeDictionary):
    """Code dictionary."""
    pass


class Name(NameDictionary):
    """Name dictionary."""
    pass


class Description(DescriptionDictionary):
    """Description dictionary."""
    pass


class Info(Dictionary):
    """Regular dictionary."""
    pass
