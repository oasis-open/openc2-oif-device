"""
OSQuery kva_speculative_info ORM
"""
from osquery_orm.orm import BaseModel
from peewee import IntegerField


class KvaSpeculativeInfo(BaseModel):
    """
    Display kernel virtual address and speculative execution information for the system.
    Examples:
        select * from kva_speculative_info
    """
    kva_shadow_enabled = IntegerField(help_text="Kernel Virtual Address shadowing is enabled.")
    kva_shadow_user_global = IntegerField(help_text="User pages are marked as global.")
    kva_shadow_pcid = IntegerField(help_text="Kernel VA PCID flushing optimization is enabled.")
    kva_shadow_inv_pcid = IntegerField(help_text="Kernel VA INVPCID is enabled.")
    bp_mitigations = IntegerField(help_text="Branch Prediction mitigations are enabled.")
    bp_system_pol_disabled = IntegerField(help_text="Branch Predictions are disabled via system policy.")
    bp_microcode_disabled = IntegerField(help_text="Branch Predictions are disabled due to lack of microcode update.")
    cpu_spec_ctrl_supported = IntegerField(help_text="SPEC_CTRL MSR supported by CPU Microcode.")
    ibrs_support_enabled = IntegerField(help_text="Windows uses IBRS.")
    stibp_support_enabled = IntegerField(help_text="Windows uses STIBP.")
    cpu_pred_cmd_supported = IntegerField(help_text="PRED_CMD MSR supported by CPU Microcode.")

    class Meta:
        table_name = "kva_speculative_info"
