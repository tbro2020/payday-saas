from slick_reporting.views import ReportView, Chart
from slick_reporting.fields import ComputationField
from payroll.models import ItemPaid
from django.db.models import Sum

class ReportItemPaid(ReportView):
    report_model = ItemPaid
    group_by = "name"
    filters = []

    columns = [
        "name",
        ComputationField.create(method=Sum, field="amount_qp_employee", name="amount_qp_employee__sum", verbose_name="Total"),
    ]

    chart_settings = [
        Chart(
            "Paie",
            Chart.PIE,
            data_source=["amount_qp_employee__sum"],
            title_source=["name"],
        ),
    ]