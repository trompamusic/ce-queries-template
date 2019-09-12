# from cequery import StringConstant, make_parameters
# from cequery import wikipedia
# from cequery.person import get_wikidata_url

from . import StringConstant, make_parameters, MUTATION
from .templates import mutation_create

MUTATION = '''mutation {{
  {mutation}
}}
'''

CREATE_MUSIC_COMPOSITION = '''
CreateMusicComposition(
  {parameters}
) {{
  identifier
  name
  relation
}}
'''

UPDATE_MUSIC_COMPOSITION = '''
UpdateMusicComposition(
  {parameters}
) {{
  identifier
  name
  relation
}}
'''

ADD_COMPOSITION_AUTHOR = '''
AddCreativeWorkInterfaceLegalPerson(
  from: {{identifier: "{composition_id}" type:MusicComposition}}
  to: {{identifier: "{composer_id}" type: Person}}
  field: author 
)
{{
    from {{
        ... on CreativeWork {{
            identifier, contributor
    }}
  }}
  to {{
        ... on Person {{
            identifier, contributor
    }}
  }}
}}
'''

REMOVE_COMPOSITION_AUTHOR = '''
RemoveCreativeWorkInterfaceLegalPerson(
  from: {{identifier: "{composition_id}" type:MusicComposition}}
  to: {{identifier: "{composer_id}" type: Person}}
  field: author 
)
{{
    from {{
        ... on CreativeWork {{
            identifier, contributor
    }}
  }}
  to {{
        ... on Person {{
            identifier, contributor
    }}
  }}
}}
'''


def get_query_add_composition_author(composition_id, composer_id):
    query = ADD_COMPOSITION_AUTHOR.format(composition_id=composition_id, composer_id=composer_id)
    return MUTATION.format(mutation=query)


def get_query_remove_composition_author(composition_id, composer_id):
    query = REMOVE_COMPOSITION_AUTHOR.format(composition_id=composition_id, composer_id=composer_id)
    return MUTATION.format(mutation=query)


def get_composer_rel(mb_work):
    # The relation type for artist-url relation type
    composer_rel_type = "d59d99ea-23d4-4a80-b066-edca32ee158f"
    for l in mb_artist.get("artist-relation-list", []):
        if l["type-id"] == composer_rel_type:
            return l["artist"]
    return None


def transform_musicbrainz_work(mb_work):
    """Transform a musicbrainz artist to a CreatePerson mutation for the CE"""

    # possible languages: en,es,ca,nl,de,fr

    wikidata_url = get_wikidata_url(mb_artist)
    description = ""
    if wikidata_url:
        description = wikipedia.get_description_for_wikidata(wikidata_url)

    artist = get_composer_rel(mb_work)
    if not artist:
        print("unknown artist")
        artist = {"name": "Unknown"}

    work_name = mb_work["name"]
    args = {
        "title": work_name,
        "name": work_name,
        "publisher": "https://musicbrainz.org",
        "contributor": "https://musicbrainz.org",
        "creator": artist,
        "source": "https://musicbrainz.org/work/{}".format(mb_work["id"]),
        "subject": "artist",
        "description": description,
        "format": "text/html",  # a work doesn't have a mimetype, use the mimetype of the source (musicbrainz page)
        # TODO: do works have a languange?
        "language": StringConstant("en"),
            }
    create_music_composition = CREATE_MUSIC_COMPOSITION.format(parameters=make_parameters(**args))
    return MUTATION.format(mutation=create_music_composition)


def transform_data_update_composition(identifier, composition):
    """Transform a work from a data file to a UpdateMusicComposition mutation for the CE"""

    # required params: contributor, creator, description, format, language, source,
    # subject, title, name, identifer

    args = _transform_data_create_composition(composition)
    args["identifier"] = identifier
    update_music_composition = UPDATE_MUSIC_COMPOSITION.format(parameters=make_parameters(**args))
    return MUTATION.format(mutation=update_music_composition)


def _transform_data_create_composition(composition):
    """Transform a work from a data file to a CreateMusicComposition mutation for the CE"""

    # required params: contributor, creator, description, format, language, source,
    # subject, title, name

    desc = composition.get("Description",
                           "Composition {} by {}".format(composition["Title"], composition["Creator"]["Name"]))

    args = {
        "title": composition["Title"],
        "name": composition["Title"],
        "contributor": composition["Contributor"],
        "creator": composition["Creator"]["Name"],
        "description": desc,
        "source": composition["Source"],
        # "publisher": composition["Publisher"],
        "subject": composition["Subject"],
        # The format of the source page
        "format": "text/html",
        # The language of the source page
        "language": StringConstant(composition["Language"]),
            }
    return args


def mutation_create_composition(composition_name: str, publisher: str, contributor: str, creator: str, source: str, description: str, subject: str, language: str):
    """Returns a mutation for creating a digital document object
    Arguments:
        str comosition_name: The name of the comnposition.
        str publisher: The person, organization or service responsible for making the artist inofrmation available.
        str contributor: A person, an organization, or a service responsible for contributing the artist to the web resource. This can be either a name or a base URL.
        str creator: The person, organization or service who created the thing the web resource is about.
        srt sourcer: The URL of the web resource to be represented by the node.
        str description: An account of the artist. 
        str language: The language the metadata is written in. Currently supported languages are en,es,ca,nl,de,fr.


    Returns:
        The string for the mutation for creating the artist.
    Raises:
        Assertion error if the input language is not one of the supported languages. 
    """
    return mutation_create(composition_name, publisher, contributor, creator, source, description, language, subject, CREATE_MUSIC_COMPOSITION)

def mutation_update_document(identifier:str, composition_name=None, publisher=None, contributor=None, creator=None, source=None, description=None, language=None):
    """Returns a mutation for updating a person object
    Arguments:
        identifier: The unique identifier of the composition.
        composition_name (optional): The name of the composition.
        publisher (optional): The person, organization or service responsible for making the artist inofrmation available.
        contributor (optional): A person, an organization, or a service responsible for contributing the artist to the web resource. This can be either a name or a base URL.
        creator (optional): The person, organization or service who created the composition that the web resource is about.
        sourcer (optional): The URL of the web resource to be represented by the node.
        description (optional): An account of the artist. 
        language (optional): The language the metadata is written in. Currently supported languages are en,es,ca,nl,de,fr.
    Returns:
        The string for the mutation for creating the artist.
    Raises:
        Assertion error if the input language is not one of the supported languages. 
    """

    return mutation_update(identifier, UPDATE_MUSIC_COMPOSITION, composition_name, publisher, contributor, creator, source, description, language)
