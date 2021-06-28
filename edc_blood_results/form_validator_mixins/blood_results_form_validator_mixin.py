from edc_constants.constants import YES
from edc_lab.form_validators import CrfRequisitionFormValidatorMixin
from edc_reportable import ReportablesFormValidatorMixin


class BloodResultsFormValidatorMixin(
    ReportablesFormValidatorMixin,
    CrfRequisitionFormValidatorMixin,
):

    requisition_field = "requisition"
    assay_datetime_field = "assay_datetime"
    value_field_suffix = "_value"
    panel = None
    poc_panel = None

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

        for utest_id in self.panel.utest_ids:
            try:
                utest_id = utest_id.split(self.value_field_suffix)
            except ValueError:
                pass
            if f"{utest_id}_units" in self.cleaned_data:
                self.required_if_not_none(
                    field=f"{utest_id}{self.value_field_suffix or ''}",
                    field_required=f"{utest_id}_units",
                    field_required_evaluate_as_int=True,
                )
            if f"{utest_id}_abnormal" in self.cleaned_data:
                self.required_if_not_none(
                    field=f"{utest_id}{self.value_field_suffix or ''}",
                    field_required=f"{utest_id}_abnormal",
                    field_required_evaluate_as_int=True,
                )
            if f"{utest_id}_reportable" in self.cleaned_data:
                self.required_if_not_none(
                    field=f"{utest_id}{self.value_field_suffix or ''}",
                    field_required=f"{utest_id}_reportable",
                    field_required_evaluate_as_int=True,
                )

        self.validate_reportable_fields(
            reference_list_name=self.reference_list_name,
            **self.reportables_evaluator_options,
        )
