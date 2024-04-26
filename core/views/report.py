from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import ComputationField
from payroll.models import Payroll
from django.db.models import Sum

class Reporter(ReportView):
    report_model = Payroll
    group_by = "name"
    filters = []

    columns = [
        "name",
        ComputationField.create(method=Sum, field="overall_net", name="overall_net__sum", verbose_name="Total"),
    ]

    chart_settings = [
        Chart(
            "Paie",
            Chart.BAR,
            data_source=["overall_net__sum"],
            title_source=["name"],
        ),
    ]