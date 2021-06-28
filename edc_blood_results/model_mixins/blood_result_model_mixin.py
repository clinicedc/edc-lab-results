from django.apps import apps as django_apps
from django.db import models
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_reportable import site_reportables


class BloodResultsFieldsModelMixin(models.Model):

    results_abnormal = models.CharField(
        verbose_name="Are any of the above results abnormal?",
        choices=YES_NO,
        max_length=25,
    )

    results_reportable = models.CharField(
        verbose_name="If any results are abnormal, are results within grade 3 " "or above?",
        max_length=25,
        choices=YES_NO_NA,
        help_text="If YES, this value will open Adverse Event Form.",
    )

    summary = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class BloodResultsMethodsModelMixin(models.Model):
    def save(self, *args, **kwargs):
        self.summary = "\n".join(self.get_summary())
        super().save(*args, **kwargs)

    def get_summary_options(self):
        model_cls = django_apps.get_model("edc_registration.registeredsubject")
        registered_subject = model_cls.objects.get(
            subject_identifier=self.subject_visit.subject_identifier
        )
        return dict(
            gender=registered_subject.gender,
            dob=registered_subject.dob,
            report_datetime=self.subject_visit.report_datetime,
        )

    def get_summary(self):
        opts = self.get_summary_options()
        summary = []
        for field_name in [f.name for f in self._meta.fields]:
            try:
                label, _ = field_name.split(self.value_field_suffix)
            except ValueError:
                label = field_name
            if grp := site_reportables.get(self.reportables_group_name).get(label):
                if value := getattr(self, field_name):
                    units = getattr(self, f"{label}{self.units_field_suffix}")
                    opts.update(units=units)
                    grade = grp.get_grade(value, **opts)
                    if grade and grade.grade:
                        summary.append(f"{field_name}: {grade.description}.")
                    elif not grade:
                        normal = grp.get_normal(value, **opts)
                        if not normal:
                            summary.append(f"{field_name}: {value} {units} is abnormal")
        return summary

    def get_action_item_reason(self):
        return self.summary

    @property
    def abnormal(self):
        return self.results_abnormal

    @property
    def reportable(self):
        return self.results_reportable

    class Meta:
        abstract = True


class BloodResultsModelMixin(
    BloodResultsFieldsModelMixin, BloodResultsMethodsModelMixin, models.Model
):
    """For each `result` the field name or its prefix should
    match with a value in reportables.

    For example:
        field_name = creatinine_value
        reportables name: creatinine
        value_field_suffix = "_value"

        -OR-

        field_name = creatinine
        reportables name: creatinine
        value_field_suffix = None
    """

    action_name = None
    reportables_group_name = "default"
    value_field_suffix = "_value"
    units_field_suffix = "_units"

    class Meta:
        abstract = True
