from django.urls import path
from payroll.views import *

app_name = 'payroll'

urlpatterns = [
    path('sheet/<int:pk>', Sheet.as_view(), name='sheet'),
    path('listing/<int:pk>', Listing.as_view(), name='listing'),
    path('synthesis/<int:pk>', Synthesis.as_view(), name='synthesis'),
    
    path('payslip/<int:pk>', Payslip.as_view(), name='payslip'),
    path('payslips/<int:pk>', Payslips.as_view(), name='payslips'),

    path('report/itempaid', ReportItemPaid.as_view(), name='report-item-paid')
]
