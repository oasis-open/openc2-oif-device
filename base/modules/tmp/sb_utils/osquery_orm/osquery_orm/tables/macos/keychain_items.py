"""
OSQuery keychain_items ORM
"""
from ...orm import BaseModel
from peewee import TextField


class KeychainItems(BaseModel):
    """
    Generic details about keychain items.
    """
    label = TextField(help_text="Generic item name")
    description = TextField(help_text="Optional item description")
    comment = TextField(help_text="Optional keychain comment")
    created = TextField(help_text="Data item was created")
    modified = TextField(help_text="Date of last modification")
    type = TextField(help_text="Keychain item type (class)")
    path = TextField(help_text="Path to keychain containing item")  # {'additional': True}

    class Meta:
        table_name = "keychain_items"
