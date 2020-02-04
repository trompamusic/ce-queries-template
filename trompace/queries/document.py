# Generate GraphQL queries pertaining to digital document objects.
from trompace.exceptions import UnsupportedLanguageException, MimeTypeException
from . import StringConstant
from .templates import query_create
from ..constants import SUPPORTED_LANGUAGES

QUERY_DIGITALDOCUMENT = '''query {{
  DigitalDocument(
  {parameters}
  )
  {{
    identifier
    name
    publisher
    contributor
    creator
    source
    description
    language
  }}
}}'''

QUERY_DIGITALDOCUMENT_ALL = '''query {
  DigitalDocument
  {
    identifier
    name
    publisher
    contributor
    creator
    source
    description
    language
  }
}'''



def query_document(identifier: str=None, document_name=None, publisher=None, contributor=None, creator=None,
                             source=None, description=None, language=None):
    """Returns a query for a digital document object
    Arguments:
        identifier: The unique identifier of the digital document.
        document_name: The name of the digital document.
        publisher: The person, organization or service responsible for making the artist information available.
        contributor: A person, an organization, or a service responsible for contributing the artist to the web resource.
            This can be either a name or a base URL.
        creator: The person, organization or service who created the thing the web resource is about.
        source: The URL of the web resource to be represented by the node.
        description: An account of the artist.
        language: The language the metadata is written in. Currently supported languages are en,es,ca,nl,de,fr


    Returns:
        The string for the mutation for creating the document object.
    Raises:
        UnsupportedLanguageException if the input language is not one of the supported languages.
    """
    if language and language not in SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageException(language)

    if identifier:
        return query_create(identifier, QUERY_DIGITALDOCUMENT, document_name, publisher, contributor, creator,
                                 source, description, language)
    else:
        return QUERY_DIGITALDOCUMENT_ALL 
