# Generate GraphQL queries for mutations pertaining to media object objects.
from trompace import StringConstant, _Neo4jDate, check_required_args, filter_none_args, docstring_interpolate
from trompace.constants import SUPPORTED_LANGUAGES
from trompace.exceptions import UnsupportedLanguageException, NotAMimeTypeException
from trompace.mutations.templates import format_mutation, format_link_mutation

MEDIAOBJECT_ARGS_DOCS = """name: The name of the media object.
        description: An account of the media object.
        date: The date associated with the media object.
        creator: The person, organization or service who created the thing the web resource is about.
        contributor: A person, an organization, or a service responsible for contributing the media object to the web resource. This can be either a name or a base URL.
        format_: A MimeType of the format of the page describing the media object.
        encodingFormat: A MimeType of the format of object encoded by the media object.
        source: The URL of the web resource about this media object. If no such resource is available, use the
                same value as contentUrl.
        subject: The subject of the media object.
        contentUrl: The URL of the content encoded by the media object.
        url: 
        license: 
        language: The language the metadata is written in. Currently supported languages are en,es,ca,nl,de,fr
        inLanguage: The language of the media object.
        title: The title of the resource indicated by `source`"""


@docstring_interpolate("mediaobject_args", MEDIAOBJECT_ARGS_DOCS)
def mutation_create_media_object(*, title: str, contributor: str, creator: str, source: str, format_: str,
                                 name: str = None, description: str = None, date: str = None,
                                 encodingformat: str = None, embedurl: str = None, url: str = None,
                                 contenturl: str = None, language: str = None, inlanguage: str = None,
                                 license: str = None):
    """Returns a mutation for creating a media object object.

    Arguments:
        {mediaobject_args}

    Returns:
        The string for the mutation for creating the media object.

    Raises:
        UnsupportedLanguageException if the input language is not one of the supported languages.
    """
    check_required_args(title=title, contributor=contributor, creator=creator, source=source, format_=format_)
    if language is not None and language not in SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageException(language)

    if "/" not in format_:
        raise NotAMimeTypeException(format_)

    if encodingformat is not None and "/" not in encodingformat:
        raise NotAMimeTypeException(encodingformat)

    args = {
        "title": title,
        "contributor": contributor,
        "creator": creator,
        "source": source,
        "format": format_,
        "name": name,
        "description": description,
        "encodingFormat": encodingformat,
        "embedUrl": embedurl,
        "url": url,
        "license": license,
        "contentUrl": contenturl,
        "inLanguage": inlanguage,
    }

    if date is not None:
        args["date"] = _Neo4jDate(date)
    if language is not None:
        args["language"] = StringConstant(language.lower())

    args = filter_none_args(args)

    return format_mutation("CreateMediaObject", args)


@docstring_interpolate("mediaobject_args", MEDIAOBJECT_ARGS_DOCS)
def mutation_update_media_object(identifier: str, *, name: str = None, title: str = None, description: str = None,
                                 date: str = None, creator: str = None, contributor: str = None,
                                 format_: str = None, encodingformat: str = None, source: str = None, license: str = None,
                                 subject: str = None, contenturl: str = None, language: str = None, inlanguage:str = None):
    """Returns a mutation for updating a media object object.

    Arguments:
        identifier: The identifier of the media object in the CE to be updated.
        {mediaobject_args}

    Returns:
        The string for the mutation for updating the media object.

    Raises:
        Assertion error if the input language or inLanguage is not one of the supported languages.
    """
    if format_ is not None and "/" not in format_:
        raise NotAMimeTypeException(format_)

    if encodingformat is not None and "/" not in encodingformat:
        raise NotAMimeTypeException(encodingformat)

    if language is not None and language not in SUPPORTED_LANGUAGES:
        raise UnsupportedLanguageException(language)

    args = {
        "identifier": identifier,
        "name": name,
        "title": title,
        "description": description,
        "creator": creator,
        "contributor": contributor,
        "format": format_,
        "encodingFormat": encodingformat,
        "source": source,
        "subject": subject,
        "contentUrl": contenturl,
        "license": license,
        "inLanguage": inlanguage,
    }
    if date:
        args["date"] = _Neo4jDate(date)
    if language:
        args["language"] = StringConstant(language.lower())

    args = filter_none_args(args)

    return format_mutation("UpdateMediaObject", args)


def mutation_delete_media_object(identifier: str):
    """Returns a mutation for deleting a media object object based on the identifier.

    Arguments:
        identifier: The unique identifier of the media object object.

    Returns:
        The string for the mutation for deleting the media object object based on the identifier.
    """

    return format_mutation("DeleteMediaObject", {"identifier": identifier})


def mutation_merge_media_object_work_example(media_object_identifier: str, work_identifier: str):
    """Returns a mutation for creating merging a media object as an example of a work.

    Arguments:
        media_object_identifier: The unique identifier of the media object.
        work_identifier: The unique identifier of the work that the media object is an example of.

    Returns:
        The string for the mutation for merging a media object as an example of the work.
    """

    return format_link_mutation("MergeMediaObjectExampleOfWork", media_object_identifier, work_identifier)


def mutation_remove_media_object_work_example(media_object_identifier: str, work_identifier: str):
    """Returns a mutation for creating removing a media object as an example of a work.

    Arguments:
        media_object_identifier: The unique identifier of the media object.
        work_identifier: The unique identifier of the work that the media object is an example of.

    Returns:
        The string for the mutation for removing a media object as an example of the work.
    """

    return format_link_mutation("RemoveMediaObjectExampleOfWork", media_object_identifier, work_identifier)


def mutation_merge_media_object_encoding(media_object_identifier_1: str, media_object_identifier_2: str):
    """Returns a mutation for creating merging a media object as an encoding of another media object.

    Arguments:
        media_object_identifier_1: The unique identifier of the media object that is encoding the other.
        media_object_identifier_2: The unique identifier of the media object being encoded.

    Returns:
        The string for the mutation for merging a media object as an encoding of another media object.
    """

    return format_link_mutation("MergeMediaObjectEncoding", media_object_identifier_1, media_object_identifier_2)


def mutation_remove_media_object_encoding(media_object_identifier_1: str, media_object_identifier_2: str):
    """Returns a mutation for creating removing a media object as an encoding of another media object.

    Arguments:
        media_object_identifier_1: The unique identifier of the media object that is encoding the other.
        media_object_identifier_2: The unique identifier of the media object being encoded.

    Returns:
        The string for the mutation for removing a media object as an encoding of another media object.
    """

    return format_link_mutation("RemoveMediaObjectEncoding", media_object_identifier_1, media_object_identifier_2)
