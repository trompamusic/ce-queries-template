from graphql import validation
from typing import Optional, List
from trompace import (docstring_interpolate, filter_none_args,
                      StringConstant, check_required_args)
from trompace.constants import ItemListOrderType
from trompace.mutations import _verify_additional_type
from trompace.mutations.templates import (format_mutation, format_link_mutation,
                                          format_sequence_mutation, format_sequence_link_mutation)
import trompace.exceptions

ITEMLIST_ARGS_DOCS = """name: The name of the ItemList object.
        creator: The person, organization or service who created the ItemList.
        itemlistorder: The type of ordering for the list (ascending, descending, unordered, ordered)
        contributor (optional): A person, an organization, or a service responsible
          for contributing the ItemList to the web resource. This can be either a name or a base URL.
        description (optional): The description of the ItemList object
        additionaltype (optional): A list of schema.org additionalTypes used to categorise this ItemList
        """


@docstring_interpolate("itemlist_args", ITEMLIST_ARGS_DOCS)
def mutation_create_itemlist(name: str, creator: str,
                             itemlistorder: ItemListOrderType = ItemListOrderType.ItemListUnordered,
                             description: str = None, contributor: str = None, additionaltype: List[str] = None):
    """Returns a mutation for creating an ItemList object.
    (https://schema.org/ItemList)

    Arguments:
        {itemlist_args}

    Returns:
        The string for the mutation for creating the ItemList.
    """
    if not isinstance(itemlistorder, ItemListOrderType):
        raise trompace.exceptions.InvalidItemListOrderTypeException(itemlistorder)
    check_required_args(name=name, creator=creator)
    additionaltype = _verify_additional_type(additionaltype)

    args = {
        "creator": creator,
        "name": name,
        "contributor": contributor,
        "description": description,
        "additionalType": additionaltype
    }
    if itemlistorder:
        args["itemListOrder"] = StringConstant(itemlistorder)

    args = filter_none_args(args)

    return format_mutation("CreateItemList", args)


@docstring_interpolate("itemlist_args", ITEMLIST_ARGS_DOCS)
def mutation_update_itemlist(identifier: str, name: str = None, creator: str = None,
                             itemlistorder: ItemListOrderType = None,
                             description: str = None, contributor: str = None,
                             additionaltype: List[str] = None):
    """Returns a mutation for updating an ItemList object.
    (https://schema.org/ItemList)

    Arguments:
        identifier: The identifier of the ItemList in the CE to be updated.
        {itemlist_args}

    Returns:
        The string for the mutation for updating the ItemList.
    """
    if itemlistorder is not None and not isinstance(itemlistorder, ItemListOrderType):
        raise trompace.exceptions.InvalidItemListOrderTypeException(itemlistorder)
    check_required_args(identifier=identifier)
    additionaltype = _verify_additional_type(additionaltype)

    args = {
        "identifier": identifier,
        "contributor": contributor,
        "name": name,
        "description": description,
        "creator": creator,
        "additionalType": additionaltype,
    }
    if itemlistorder is not None:
        args["itemListOrder"] = StringConstant(itemlistorder)

    args = filter_none_args(args)

    return format_mutation("UpdateItemList", args)


def mutation_delete_itemlist(identifier: str):
    """Returns a mutation for deleting an ItemList object based
    on the identifier.
    (https://schema.org/ItemList)

    Arguments:
        identifier: The unique identifier of the ItemList object.

    Returns:
        The string for the mutation for deleting the ItemList object
        based on the identifier.
    """

    return format_mutation("DeleteItemList", {"identifier": identifier})


LISTITEM_ARGS_DOCS = """name: The name of the ListItem object.
        creator: The person, organization or service who created the ListItem.
        contributor: A person, an organization, or a service responsible for contributing the ListItem to the web resource.
          This can be either a name or a base URL.
        description: The description of the ListItem object
        itemurl: If the item of this ListItem points to a URL outside of the CE, the item URL 
        position: the position of the ListItem
        """


@docstring_interpolate("listitem_args", LISTITEM_ARGS_DOCS)
def mutation_create_listitem(creator: str, name: str = None, contributor: str = None,
                             description: str = None, itemurl: str = None, position: Optional[int] = None):
    """Returns a mutation for creating a ListItem object.
    (https://schema.org/ListItem)

    Arguments:
        {listitem_args}

    Returns:
        The string for the mutation for creating the ListItem.
    """
    check_required_args(creator=creator)
    args = {
        "contributor": contributor,
        "name": name,
        "creator": creator,
        "description": description,
        "itemUrl": itemurl,
        "position": position,
    }

    args = filter_none_args(args)

    return format_mutation("CreateListItem", args)


@docstring_interpolate("listitem_args", LISTITEM_ARGS_DOCS)
def mutation_update_listitem(identifier: str, creator: str = None, name: str = None, contributor: str = None,
                             description: str = None, itemurl: str = None, position: int = None):
    """Returns a mutation for updating a ListItem object.
    (https://schema.org/ListItem)

    Arguments:
        identifier: The identifier of the ListItem in the CE to be updated.
        {listitem_args}

    Returns:
        The string for the mutation for updating the ListItem.
    """
    args = {
        "identifier": identifier,
        "creator": creator,
        "name": name,
        "contributor": contributor,
        "description": description,
        "itemUrl": itemurl,
        "position": position,
    }

    args = filter_none_args(args)

    return format_mutation("UpdateListItem", args)


def mutation_delete_listitem(identifier: str):
    """Returns a mutation for deleting a ListItem object based on the
    identifier.
    (https://schema.org/ListItem)

    Arguments:
        identifier: The unique identifier of the ListItem object.

    Returns:
        The string for the mutation for deleting the ListItem object based
        on the identifier.
    """
    return format_mutation("DeleteListItem", {"identifier": identifier})


def mutation_add_listitem_nextitem(listitem_id: str, nextitem_id: str):
    """Returns a mutation for adding a NextItem to a ListItem object
    based on the identifier.
    (https://schema.org/nextItem)

    Arguments:
        listitem_id: The unique identifier of the ListItem object.
        nextitem_id: The unique identifier of the NextItem object.

    Returns:
        The string for the mutation for adding a NextItem to a ListItem object
    based on the identifier.
    """
    check_required_args(listitem_id=listitem_id, nextitem_id=nextitem_id)
    return format_link_mutation("MergeListItemNextItem", listitem_id,
                                nextitem_id)


def mutation_remove_listitem_nextitem(listitem_id: str, nextitem_id: str):
    """Returns a mutation for removing a NextItem from a ListItem object
    based on the identifier.
    (https://schema.org/nextItem)

    Arguments:
        listitem_id: The unique identifier of the ListItem object.
        nextitem_id: The unique identifier of the NextItem object.

    Returns:
        The string for the mutation for removing a NextItem from a ListItem
    object based on the identifier.
    """
    check_required_args(listitem_id=listitem_id, nextitem_id=nextitem_id)
    return format_link_mutation("RemoveListItemNextItem", listitem_id,
                                nextitem_id)


def mutation_add_listitem_item(listitem_id: str, item_id: str):
    """Returns a mutation for adding an Item to a ListItem object
    based on the identifier.
    (https://schema.org/item)

    Arguments:
        listitem_id: The unique identifier of the ListItem object.
        item_id: The unique identifier of the Item object.

    Returns:
        The string for the mutation for adding a Item to a ListItem object
    based on the identifier.
    """
    check_required_args(listitem_id=listitem_id, item_id=item_id)
    return format_link_mutation("MergeListItemItem", listitem_id, item_id)


def mutation_remove_listitem_item(listitem_id: str, item_id: str):
    """Returns a mutation for removing a Item from a ListItem object
    based on the identifier.
    (https://schema.org/item)

    Arguments:
        listitem_id: The unique identifier of the ListItem object.
        item_id: The unique identifier of the Item object.

    Returns:
        The string for the mutation for removing a Item from a ListItem
    object based on the identifier.
    """
    check_required_args(listitem_id=listitem_id, item_id=item_id)
    return format_link_mutation("RemoveListItemItem", listitem_id, item_id)


def mutation_add_itemlist_itemlist_element(itemlist_id: str, element_id: str):
    """Returns a mutation for adding a ThingInterface in an ItemList object based
    on the identifier.
    (https://schema.org/itemListElement)

    Arguments:
        itemlist_id: The unique identifier of the ItemList object.
        element_id: The unique identifier of the ThingInterface object.

    Returns:
        The string for the mutation for adding an ThingInterface in an ItemList object
        based on the identifier,
    """
    check_required_args(itemlist_id=itemlist_id, element_id=element_id)
    return format_link_mutation("MergeItemListItemListElement", itemlist_id,
                                element_id)


def mutation_remove_itemlist_itemlist_element(itemlist_id: str,
                                              element_id: str):
    """Returns a mutation for removing a ThingInterface from an ItemList object
    based on the identifier.
    (https://schema.org/itemListElement)

    Arguments:
        itemlist_id: The unique identifier of the ItemList object.
        element_id: The unique identifier of the ThingInterface object.

    Returns:
        The string for the mutation for removing an ThingInterface from an ItemList
        object based on the identifier.
    """
    check_required_args(itemlist_id=itemlist_id, element_id=element_id)
    return format_link_mutation("RemoveItemListItemListElement", itemlist_id,
                                element_id)


LISTITEM_SEQ_ARGS_DOCS = """listitems: the ListItems objects to create
        creator: The person, organization or service who created the items.
        contributor: A person, an organization, or a service responsible for contributing the ListItem to
          the web resource. This can be either a name or a base URL.
        name: The name of the ListItem object.
        """


@docstring_interpolate("listitem_args", LISTITEM_SEQ_ARGS_DOCS)
def mutation_sequence_create_listitem(listitems: list, contributor: str, creator: str = None,
                                      name: str = None, description: list = None):
    """Returns a mutation for creating a sequence of ListItem objects
    (https://schema.org/itemListElement)

    Arguments:
        {listitem_args}

    Returns:
        The string for the mutation for creating a sequence of ListItem objects
    """
    mutation_list = []

    mutationname = "CreateListItem"
    for pos, listitem in enumerate(listitems):
        args = {
            "contributor": contributor,
            "name": name,
            "creator": creator,
            "description": description[pos],
            "position": pos,
        }
        mutationalias = "ListItemAlias{}".format(pos)
        mutation_list.append((mutationalias, mutationname, args))

    return format_sequence_mutation(mutations=mutation_list)


def mutation_sequence_add_itemlist_itemlist_element(itemlist_id: str,
                                                    element_ids: list):
    """Returns a mutation for adding a sequence of ThingInterface in an
    ItemList object based on the identifiers.
    (https://schema.org/itemListElement)

    Arguments:
        itemlist_id: The unique identifier of the ItemList object.
        element_ids: The list of unique identifiers of the ThingInterface objects.

    Returns:
        The string for the mutation for adding a sequence of ThingInterface in an
        ItemList object based on the identifiers.
    """
    check_required_args(itemlist_id=itemlist_id, element_ids=element_ids)

    mutation_list = []

    mutationname = "MergeItemListItemListElement"
    for pos, element_id in enumerate(element_ids):
        args = [itemlist_id, element_id]
        mutationalias = "MergeItemListItemListElementAlias{}".format(pos)
        mutation_list.append((mutationalias, mutationname, args))

    return format_sequence_link_mutation(mutations=mutation_list)


def mutation_sequence_add_listitem_item(listitem_ids: list,
                                        item_ids: list):
    """Returns a mutation for adding a sequence of ThingInterface in an
    ListItem objects based on the identifiers.
    (https://schema.org/itemListElement)

    Arguments:
        listitem_ids: The list of unique identifiers of the ListItem objects.
        item_ids: The list of unique identifiers of the ThingInterface objects.

    Returns:
        The string for the mutation for adding a sequence of ThingInterface in an
    ListItem objects based on the identifiers.
    """
    check_required_args(listitem_ids=listitem_ids, item_ids=item_ids)

    mutation_list = []

    mutationname = "MergeListItemItem"
    for pos, _ in enumerate(listitem_ids):
        args = [listitem_ids[pos], item_ids[pos]]
        mutationalias = "MergeListItemItemAlias{}".format(pos)
        mutation_list.append((mutationalias, mutationname, args))

    return format_sequence_link_mutation(mutations=mutation_list)


def mutation_sequence_add_listitem_nextitem(listitem_ids: list):
    """Returns a mutation for adding a sequence of NextItem to an
    ListItem objects based on the identifiers.
    (https://schema.org/itemListElement)

    Arguments:
        listitem_ids: The list of unique identifier of the ListItems objects.

    Returns:
        The string for the mutation for adding a sequence of NextItem to an
    ListItem objects based on the identifiers.
    """
    check_required_args(listitem_ids=listitem_ids)

    mutation_list = []

    mutationname = "MergeListItemNextItem"
    pos = 0
    while pos+1 < len(listitem_ids):
        args = [listitem_ids[pos], listitem_ids[pos+1]]
        mutationalias = "MergeListItemNextItemAlias{}".format(pos)
        mutation_list.append((mutationalias, mutationname, args))
        pos += 1

    return format_sequence_link_mutation(mutations=mutation_list)
