"""
OSQuery pci_devices ORM
"""
from ....orm import BaseModel
from peewee import TextField


class PciDevices(BaseModel):
    """
    PCI devices active on the host system.
    """
    pci_slot = TextField(help_text="PCI Device used slot")
    pci_class = TextField(help_text="PCI Device class")
    driver = TextField(help_text="PCI Device used driver")
    vendor = TextField(help_text="PCI Device vendor")
    vendor_id = TextField(help_text="Hex encoded PCI Device vendor identifier")
    model = TextField(help_text="PCI Device model")
    model_id = TextField(help_text="Hex encoded PCI Device model identifier")

    class Meta:
        table_name = "pci_devices"


# OS specific properties for Linux
class Linux_PciDevices(PciDevices):
    pci_class_id = TextField(help_text="PCI Device class ID in hex format")
    pci_subclass_id = TextField(help_text="PCI Device  subclass in hex format")
    pci_subclass = TextField(help_text="PCI Device subclass")
    subsystem_vendor_id = TextField(help_text="Vendor ID of PCI device subsystem")
    subsystem_vendor = TextField(help_text="Vendor of PCI device subsystem")
    subsystem_model_id = TextField(help_text="Model ID of PCI device subsystem")
    subsystem_model = TextField(help_text="Device description of PCI device subsystem")

    class Meta:
        table_name = "pci_devices"
