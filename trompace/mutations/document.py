# Generate GraphQL queries for mutations pertaining to digital document objects.
from trompace.exceptions import UnsupportedLanguageException
from .templates import mutation_create, mutation_delete, mutation_update, mutation_link
from . import StringConstant

# We say that 2 different scores of the same thing are a broad match
from ..constants import SUPPORTED_LANGUAGES

ADD_DIGITAL_DOCUMENT_BROAD_MATCH = '''AddDigitalDocumentBroadMatch(
    from: {{identifier: "{identifier_1}" }}
    to: {{identifier: "{identifier_2}" }}
  ) {{
    from {{
      identifier
    }}
    to {{
      identifier
    }}
  }}'''

REMOVE_DIGITAL_DOCUMENT_BROAD_MATCH = '''RemoveDigitalDocumentBroadMatch(
    from: {{identifier: "{identifier_1}" }}
    to: {{identifier: "{identifier_2}" }}
  ) {{
    from {{
      identifier
    }}
    to {{
      identifier
    }}
  }}'''

ADD_DIGITAL_DOCUMENT_SUBJECT_OF_COMPOSITION = '''AddThingInterfaceCreativeWorkInterface(
    from: {{identifier: "{identifier_1}" type:DigitalDocument}}
    to: {{identifier: "{identifier_2}" type:MusicComposition}}
    field: subjectOf
  ) {{
      from {{
        __typename
      }}
      to {{
        __typename
      }}
  }}'''

REMOVE_DIGITAL_DOCUMENT_SUBJECT_OF_COMPOSITION = '''RemoveThingInterfaceCreativeWorkInterface(
    from: {{identifier: "{identifier_1}" type:DigitalDocument}}
    to: {{identifier: "{identifier_2}" type:MusicComposition}}
    field: subjectOf
  ) {{
      from {{
        __typename
      }}
      to {{
        __typename
      }}
  }}'''

CREATE_DIGITAL_DOCUMENT = '''CreateDigitalDocument(
        {parameters}
  ) {{
    identifier
  }}'''

UPDATE_DIGITAL_DOCUMENT = '''UpdateDigitalDocument(
        {parameters}
) {{
  identifier
}}'''

DELETE_DIGITAL_DOCUMENT = '''DeleteDigitalDocument(
    {parameters}
  ) {{
    identifier
  }}'''

ADD_DIGITAL_DOCUMENT_TO_CONTROL_ACTION_MUTATION = """AddActionInterfaceThingInterface (
            from: {{identifier: "{identifier_2}", type: ControlAction}}
            to: {{identifier: "{identifier_1}", type: DigitalDocument}}
            field: result
        ) {{
            from {{
                __typename
            }}
            to {{
                __typename
            }}
        }}"""


def mutation_create_document(document_name: str, publisher: str, contributor: str, creator: str, source: str,
                             description: str, subject: str, language: str, formatin="text/html"):
    """Returns a mutation for creating a digital document object
    Arguments:
        document_name: The name of the digital document.
        publisher: The person, organization or service responsible for making the artist inofrmation available.
        contributor: A person, an organization, or a service responsible for contributing the artist to the web resource. This can be either a name or a base URL.
        creator: The person, organization or service who created the thing the web resource is about.
        sourcer: The URL of the web resource to be represented by the node.
        description: An account of the artist.
        language: The language the metadata is written in. Currently supported languages are en,es,ca,nl,de,fr


    Returns:
        The string for the mutation for creating the document object.
    Raises:
        UnsupportedLanguageException if the input language is not one of the supported languages.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageException(language)

    assert "/" in formatin, "Please provide a valid mimetype for format"

    args = {
        "title": document_name,
        "name": document_name,
        "publisher": publisher,
        "contributor": contributor,
        "creator": creator,
        "source": source,
        "subject": subject,
        "description": description,
        "format": formatin,
        "language": StringConstant(language.lower()),
    }
    return mutation_create(args, CREATE_DIGITAL_DOCUMENT)




def mutation_update_document(identifier: str, document_name=None, publisher=None, contributor=None, creator=None,
                             source=None, description=None, language=None):
    """Returns a mutation for updating a digital document object.
    Arguments:
        identifier: The unique identifier of the digital document.
        document_name (optional): The name of the digital document.
        publisher (optional): The person, organization or service responsible for making the artist inofrmation available.
        contributor (optional): A person, an organization, or a service responsible for contributing the artist to the web resource. This can be either a name or a base URL.
        creator (optional): The person, organization or service who created the document that the web resource is about.
        sourcer (optional): The URL of the web resource to be represented by the node.
        description (optional): An account of the artist.
        language (optional): The language the metadata is written in. Currently supported languages are en,es,ca,nl,de,fr.
    Returns:
        The string for the mutation for creating the artist.
    Raises:
        Assertion error if the input language is not one of the supported languages.
    """

    return mutation_update(identifier, UPDATE_DIGITAL_DOCUMENT, document_name, publisher, contributor, creator, source,
                           description, language)


def mutation_delete_document(identifier: str):
    """Returns a mutation for deleting a digital document object based on the identifier.
    Arguments:
        identifier: The unique identifier of the digital document object.
    Returns:
        The string for the mutation for deleting the digital document object based on the identifier.
    """

    return mutation_delete(identifier, DELETE_DIGITAL_DOCUMENT)


def mutation_add_broad_match_document(from_identifier: str, to_identifier: str):
    """Returns a mutation for creating a broad match between two digital document objects.
    Arguments:
        from_identifier: The unique identifier of the digital document object from which to create the broad match.
        to_identifier: The unique identifier of the digital document object to which the broad match should be created.
    Returns:
        The string for the mutation for creating the broad match between the two documents.
    """

    return mutation_link(from_identifier, to_identifier, ADD_DIGITAL_DOCUMENT_BROAD_MATCH)


def mutation_remove_broad_match_document(from_identifier: str, to_identifier: str):
    """Returns a mutation for removing a broad match between two digital document objects.
    Arguments:
        from_identifier: The unique identifier of the digital document object from which to remove the broad match.
        to_identifier: The unique identifier of the digital document object to which the broad match should be removed.
    Returns:
        The string for the mutation for removing the broad match between the two documents.
    """

    return mutation_link(from_identifier, to_identifier, REMOVE_DIGITAL_DOCUMENT_BROAD_MATCH)


def mutation_add_digital_document_subject_of_composition(document_id: str, composition_id: str):
    """Returns a mutation for adding a digital document as a subject of a composition.
    Arguments:
        document_id: The unique identifier of the digital document object.
        composition_id: The unique identifier of the composition object.
    Returns:
        The string for the mutation for adding the document as a subject of the composition.
    """

    return mutation_link(document_id, composition_id, ADD_DIGITAL_DOCUMENT_SUBJECT_OF_COMPOSITION)

def mutation_add_digital_document_controlaction(document_id: str, controlaction_id: str):
    """Returns a mutation for adding a digital document as a subject of a composition.
    Arguments:
        document_id: The unique identifier of the digital document object.
        composition_id: The unique identifier of the composition object.
    Returns:
        The string for the mutation for adding the document as a subject of the composition.
    """

    return mutation_link(document_id, controlaction_id, ADD_DIGITAL_DOCUMENT_TO_CONTROL_ACTION_MUTATION)

def mutation_remove_digital_document_subject_of_composition(document_id: str, composition_id: str):
    """Returns a mutation for removing a digital document as a subject of a composition.
    Arguments:
        document_id: The unique identifier of the digital document object.
        composition_id: The unique identifier of the composition object.
    Returns:
        The string for the mutation for removing the document as a subject of the composition.
    """

    return mutation_link(document_id, composition_id, REMOVE_DIGITAL_DOCUMENT_SUBJECT_OF_COMPOSITION)
