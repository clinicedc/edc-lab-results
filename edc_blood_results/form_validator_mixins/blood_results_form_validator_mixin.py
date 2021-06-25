from edc_constants.constants import YES
from edc_lab.form_validators import CrfRequisitionFormValidatorMixin
from edc_reportable import GRADE3, GRADE4, ReportablesFormValidatorMixin


class BloodResultsFormValidatorMixin(
    ReportablesFormValidatorMixin,
    CrfRequisitionFormValidatorMixin,
):

    reportable_grades = [GRADE3, GRADE4]
    reference_list_name = None
    requisition_field = "requisition"
    assay_datetime_field = "assay_datetime"
    value_field_suffix = "_value"
    reportable_labels = []
    panels = []
    poc_panels = []

    @property
    def field_values(self):
        return [
            self.cleaned_data.get(f) is not None for f in [f for f in self.reportable_labels]
        ]

    def clean(self):
        self.required_if_true(any(self.field_values), field_required=self.requisition_field)

        if self.cleaned_data.get("is_poc") and self.cleaned_data.get("is_poc") == YES:
            self.validate_requisition(
                self.requisition_field, self.assay_datetime_field, *self.poc_panels
            )
        else:
            self.validate_requisition(
                self.requisition_field, self.assay_datetime_field, *self.panels
            )

        for label in self.reportable_labels:
            try:
                label = label.split(self.value_field_suffix)
            except ValueError:
                pass
            if f"{label}_units" in self.cleaned_data:
                self.required_if_not_none(
                    field=f"{label}{self.value_field_suffix or ''}",
                    field_required=f"{label}_units",
                    field_required_evaluate_as_int=True,
                )
            if f"{label}_abnormal" in self.cleaned_data:
                self.required_if_not_none(
                    field=f"{label}{self.value_field_suffix or ''}",
                    field_required=f"{label}_abnormal",
                    field_required_evaluate_as_int=True,
                )
            if f"{label}_reportable" in self.cleaned_data:
                self.required_if_not_none(
                    field=f"{label}{self.value_field_suffix or ''}",
                    field_required=f"{label}_reportable",
                    field_required_evaluate_as_int=True,
                )

        self.validate_reportable_fields(
            reference_list_name=self.reference_list_name,
            **self.reportables_evaluator_options,
        )
