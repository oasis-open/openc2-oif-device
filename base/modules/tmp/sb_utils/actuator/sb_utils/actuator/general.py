import copy
import json

from io import BufferedIOBase, TextIOBase
from ipaddress import (
    ip_network,
    ip_address,
    IPv4Address,
    IPv4Network,
    IPv6Address,
    IPv6Network
)
from jsonschema import Draft7Validator, ValidationError
from typing import List, Union


def safe_load(file_obj: Union[str, BufferedIOBase, TextIOBase], *args, **kwargs) -> dict:
    """
    Safely load a json file
    :param file_obj: json file path/object to load
    :return: loaded json data
    """
    try:
        if isinstance(file_obj, (BufferedIOBase, TextIOBase)):
            return json.load(file_obj, *args, **kwargs)

        if isinstance(file_obj, str):
            with open(file_obj, "rb") as f:
                return json.load(f, *args, **kwargs)

    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(e)
    return {}


def valid_ip(ip: Union[bytes, str]) -> Union[None, IPv4Address, IPv6Address, IPv4Network, IPv6Network]:
    """
    Validate and load an IP/Network
    :param ip: IP/Network string/bytes to load
    :return: None or loaded IP/Network
    """
    if isinstance(ip, (str, bytes)):
        try:
            return ip_network(ip, strict=False) if "/" in ip else ip_address(ip)
        except ValueError as e:
            print(e)
    return None


class ValidatorJSON(Draft7Validator):
    # Custom Methods
    def iter_errors_as(self, instance: dict, _type: str) -> list:
        if self._is_exported(_type):
            if "oneOf" in self.schema:
                exp = self._get_definition(_type)
                exp_type = exp.get("type", "")
                if exp_type == "object":
                    tmp_schema = copy.deepcopy(self.schema)
                    del tmp_schema["oneOf"]
                    del tmp_schema["definitions"][_type]
                    tmp_schema.update(exp)

                    return self.iter_errors(instance, _schema=tmp_schema)
                raise TypeError(f"field type object is expected, field type: {exp_type}")

            if "properties" in self.schema:
                props = [*self.schema["properties"].keys()]
                msg_wrapper = props[props.index(_type.lower())]
                instance = {msg_wrapper: instance}
                return self.iter_errors(instance)
        raise TypeError("field type is not an exported field")

    def is_valid_as(self, instance: dict, _type: str) -> bool:
        """
        Check if the instance is good under the current schema
        :param instance: message to validate
        :param _type: type to validate against
        :return: bool - Valid/Invalid
        """
        try:
            self.validate_as(instance, _type)
            return True
        except ValidationError:
            return False

    def validate_as(self, instance: dict, _type: str) -> None:
        """
        Check if the instance is good under the current schema
        :param instance: message to validate
        :param _type: type to validate against
        :return: ...
        """
        if "oneOf" in self.schema and self._is_exported(_type):
            exp = self._get_definition(_type)
            exp_type = exp.get("type", "")
            if exp_type == "object":
                tmp_schema = copy.deepcopy(self.schema)
                del tmp_schema["oneOf"]
                del tmp_schema["definitions"][_type]
                tmp_schema.update(exp)
                return self.validate(instance, _schema=tmp_schema)
            raise TypeError(f"field type object is expected, field type: {exp_type}")

        if "properties" in self.schema and self._is_exported(_type):
            props = [*self.schema["properties"].keys()]
            msg_wrapper = props[props.index(_type.lower())]
            instance = {msg_wrapper: instance}
            return self.validate(instance)
        raise TypeError("field type is not an exported field")

    # Helper Methods
    def _is_exported(self, _type: str) -> bool:
        """
        Check if the given type if exported
        :param _type: name of type to check if exported
        :return: bool - type is exported type
        """
        exported: List[str] = []
        if "oneOf" in self.schema:
            exported = [e.get("$ref", "") for e in self.schema.get("oneOf", [])]
        elif "properties" in self.schema:
            _type = _type.lower()
            exp = {*self.schema.get("properties", {}).keys()}
            exp.update({exp.get("$ref", "") for exp in self.schema.get("properties", {}).values()})
            exported = list(exported)
        else:
            raise TypeError("Schema format invalid")
        return any(list(e.endswith(f"{_type}") for e in exported))

    def _get_definition(self, _type: str) -> dict:
        """
        Get the definition for the given type
        :param _type: type to get hte definition for
        :return: dict - type definition
        """
        return self.schema.get("definitions", {}).get(_type, {})
