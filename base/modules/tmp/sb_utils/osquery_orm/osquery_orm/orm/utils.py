from typing import List, Set, Union
from peewee import Alias, ForeignKeyField, Field, Model, SelectQuery, callable_


def _clone_set(s) -> set:
    return set(s) if s else set()


# Customized version of `https://github.com/coleifer/peewee/blob/master/playhouse/shortcuts.py`
def model_to_dict(model: Model, recurse: bool = True, backrefs: bool = False, only: Union[List[Field], Set[Field]] = None,
             exclude: Union[List[Field], Set[Field]] = None, seen: Union[list, set] = None, extra_attrs: list = None,
             fields_from_query: SelectQuery = None, max_depth: int = None, manytomany: bool = False) -> dict:
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
    max_depth = -1 if max_depth is None else max_depth
    recurse = False if max_depth == 0 else recurse
    only = _clone_set(only)
    extra_attrs = _clone_set(extra_attrs)
    should_skip = lambda n: (n in exclude) or (only and (n not in only))

    if fields_from_query is not None:
        for item in fields_from_query._returning:
            if isinstance(item, Field):
                only.add(item)
            elif isinstance(item, Alias):
                extra_attrs.add(item._alias)

    data = {}
    exclude = _clone_set(exclude)
    seen = _clone_set(seen)
    exclude |= seen
    model_class = type(model)

    if manytomany:
        for name, m2m in model._meta.manytomany.items():
            if should_skip(name):
                continue

            exclude.update((m2m, m2m.rel_model._meta.manytomany[m2m.backref]))
            for fkf in m2m.through_model._meta.refs:
                exclude.add(fkf)

            accum = []
            for rel_obj in getattr(model, name):
                accum.append(model_to_dict(
                    rel_obj,
                    recurse=recurse,
                    backrefs=backrefs,
                    only=only,
                    exclude=exclude,
                    max_depth=max_depth - 1
                ))
            data[name] = accum

    for field in model._meta.sorted_fields:
        if should_skip(field):
            continue

        field_data = model.__data__.get(field.name)
        if isinstance(field, ForeignKeyField) and recurse:
            if field_data is not None:
                seen.add(field)
                field_data = model_to_dict(
                    getattr(model, field.name),
                    recurse=recurse,
                    backrefs=backrefs,
                    only=only,
                    exclude=exclude,
                    seen=seen,
                    max_depth=max_depth - 1)
            else:
                field_data = None
        data[field.name] = field_data

    if extra_attrs:
        for attr_name in extra_attrs:
            attr = getattr(model, attr_name)
            if callable_(attr):
                data[attr_name] = attr()
            else:
                data[attr_name] = attr

    if backrefs and recurse:
        for foreign_key, rel_model in model._meta.backrefs.items():
            if foreign_key.backref == '+':
                continue
            descriptor = getattr(model_class, foreign_key.backref)
            if descriptor in exclude or foreign_key in exclude:
                continue
            if only and (descriptor not in only) and (foreign_key not in only):
                continue

            accum = []
            exclude.add(foreign_key)
            related_query = getattr(model, foreign_key.backref)

            for rel_obj in related_query:
                accum.append(model_to_dict(
                    rel_obj,
                    recurse=recurse,
                    backrefs=backrefs,
                    only=only,
                    exclude=exclude,
                    max_depth=max_depth - 1
                ))
            data[foreign_key.backref] = accum
    return data
