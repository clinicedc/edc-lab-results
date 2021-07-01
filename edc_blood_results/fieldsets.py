from django_audit_fields import audit_fieldset_tuple
from respond_labs.panels import fbc_panel

panel_conclusion_fieldset = (
    "Conclusion",
    {"fields": ("results_abnormal", "results_reportable")},
)
panel_summary_fieldset = ("Summary", {"classes": ("collapse",), "fields": ("summary",)})


class BloodResultPanelError(Exception):
    pass


class BloodResultPanel:
    def __init__(self, panel, title=None, model_cls=None):
        self.panel = panel
        self.title = title or panel.name
        self.model_cls = model_cls

    def __repr__(self):
        return f"{self.__class__.__name__}({self.panel})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.panel})"

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
            (self.title, {"fields": ["requisition", "assay_datetime"]}),
        ]
        for item in self.panel.utest_ids:
            try:
                code, title = item
            except ValueError:
                code = item
                title = code.upper()
            fieldsets.append(self.get_panel_item_fieldset(code, title=title))
        fieldsets.extend(
            [
                panel_conclusion_fieldset,
                panel_summary_fieldset,
                audit_fieldset_tuple,
            ]
        )
        return tuple(fieldsets)

    def get_panel_item_fieldset(self, code, title=None):
        if not title:
            title = code.upper()
        model_fields = [
            f"{code}_value",
            f"{code}_units",
            f"{code}_abnormal",
            f"{code}_reportable",
        ]
        if self.model_cls:
            for field in model_fields:
                try:
                    getattr(self.model_cls, field)
                except AttributeError as e:
                    raise BloodResultPanelError(f"{e}. See {self}")

        return (
            title,
            {"fields": model_fields},
        )
