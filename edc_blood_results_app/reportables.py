from edc_lab_panel.reportables import grading_data, normal_data
from edc_reportable import site_reportables

site_reportables.register(
    name="my_reportables", normal_data=normal_data, grading_data=grading_data
)
