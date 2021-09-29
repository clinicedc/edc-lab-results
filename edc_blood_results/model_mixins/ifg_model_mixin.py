from django.db import models
from edc_constants.choices import FASTING_CHOICES, YES_NO
from edc_constants.constants import FASTING
from edc_lab.choices import RESULT_QUANTIFIER
from edc_lab.constants import EQ
from edc_reportable import (
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MILLIMOLES_PER_LITER_DISPLAY,
)
from edc_reportable.choices import REPORTABLE


class IfgModelMixin(models.Model):
    """Impaired Fasting Glucose"""

    value_field_attr = "ifg_value"

    is_poc = models.CharField(
        verbose_name="Was a point-of-care test used?",
        max_length=15,
        choices=YES_NO,
        null=True,
    )
    fasting = models.CharField(
        verbose_name="Was this fasting or non-fasting?",
        max_length=25,
        choices=FASTING_CHOICES,
        null=True,
        blank=False,
    )

    ifg_value = models.DecimalField(
        verbose_name="Blood Glucose (IFG)",
        max_digits=8,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="A `HIGH` reading may be entered as 9999.99",
    )

    ifg_quantifier = models.CharField(
        max_length=10,
        choices=RESULT_QUANTIFIER,
        default=EQ,
    )

    ifg_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
            (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER_DISPLAY),
        ),
        null=True,
        blank=True,
    )

    ifg_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    ifg_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    def get_summary_options(self):
        opts = super().get_summary_options()
        fasting = True if self.fasting == FASTING else False
        opts.update(fasting=fasting)
        return opts

    class Meta:
        abstract = True
