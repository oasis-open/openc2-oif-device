from typing import List, Set, Union
from peewee import Field, Model, SelectQuery
from .utils import model_to_dict


class BaseModel(Model):
    """
    Base for all OSQuery table models
    """
    def __str__(self):
        if self._meta.primary_key is False:
            return 'No_PK'
        return str(self._pk)

    # Overrides
    def _no_operation(self, *args, **kwargs):
        raise PermissionError("Action is not permitted")

    bulk_create = _no_operation
    bulk_update = _no_operation
    create = _no_operation
    delete = _no_operation
    delete_by_id = _no_operation
    delete_instance = _no_operation
    drop_table = _no_operation
    get_or_create = _no_operation
    insert = _no_operation
    insert_from = _no_operation
    insert_many = _no_operation
    replace = _no_operation
    replace_many = _no_operation
    save = _no_operation
    set_by_id = _no_operation
    truncate_table = _no_operation
    update = _no_operation

    # Helpers
    def dict(self, recurse: bool = True, backrefs: bool = False, only: Union[List[Field], Set[Field]] = None,
             exclude: Union[List[Field], Set[Field]] = None, seen: Union[list, set] = None, extra_attrs: list = None,
             fields_from_query: SelectQuery = None, max_depth: int = None, manytomany: bool = False):
        """
        Convert a model instance (and any related objects) to a dictionary
        :param bool recurse: Whether foreign-keys should be recursed
        :param bool backrefs: Whether lists of related objects should be recursed
        :param only: A list (or set) of field instances indicating which fields should be included
        :param exclude: A list (or set) of field instances that should be excluded from the dictionary
        :param list extra_attrs: Names of model instance attributes or methods that should be included
        :param SelectQuery fields_from_query: Query that was source of model. Take fields explicitly selected by the query and serialize them
        :param int max_depth: Maximum depth to recurse, value <= 0 means no max
        :param bool manytomany: Process many-to-many fields
        """
        return model_to_dict(self, recurse, backrefs, only, exclude, seen, extra_attrs, fields_from_query, max_depth, manytomany)

    class Meta:
        primary_key = False
