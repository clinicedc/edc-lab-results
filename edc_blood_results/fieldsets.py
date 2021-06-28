from django_audit_fields import audit_fieldset_tuple
from respond_labs.panels import fbc_panel

panel_conclusion_fieldset = (
    "Conclusion",
    {"fields": ("results_abnormal", "results_reportable")},
)
panel_summary_fieldset = ("Summary", {"classes": ("collapse",), "fields": ("summary",)})


def get_panel_item_fieldset(code, title=None):
    if not title:
        title = code.upper()
    return (
        title,
        {
            "fields": [
                f"{code}_value",
                f"{code}_units",
                f"{code}_abnormal",
                f"{code}_reportable",
            ]
        },
    )


def get_panel_header_fieldset(title):
    return title, {"fields": ["requisition", "assay_datetime"]}


class BloodResultPanel:
    def __init__(self, panel, title=None):
        self.panel = panel
        self.title = title or panel.name

    @property
    def utest_ids(self):
        utest_ids = []
        for item in self.panel.utest_ids:
            try:
                utest_id, _ = item
            except ValueError:
                utest_id = item
            utest_ids.append(utest_id)
        return utest_ids

    @property
    def fieldsets(self):
        fieldsets = [
            (None, {"fields": ("subject_visit", "report_datetime")}),
            get_panel_header_fieldset(self.title),
        ]
        for item in self.panel.utest_ids:
            try:
                code, title = item
            except ValueError:
                code = item
                title = code.upper()
            fieldsets.append(get_panel_item_fieldset(code, title=title))
        fieldsets.extend(
            [
                panel_conclusion_fieldset,
                panel_summary_fieldset,
                audit_fieldset_tuple,
            ]
        )
        return tuple(fieldsets)
