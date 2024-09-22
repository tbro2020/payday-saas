from django.urls import path
from payroll.views import *

app_name = 'payroll'

urlpatterns = [
    path('canvas', Canvas.as_view(), name='canvas'),
    path('canvas-items-to-pay', CanvasItemsToPay.as_view(), name='canvas-items-to-pay'),

    path('sheet/<int:pk>', SheetSummary.as_view(), name='sheet'),
    path('listing/<int:pk>', Listing.as_view(), name='listing'),
    
    path('synthesis/employee/<int:pk>', SynthesisByEmployee.as_view(), name='synthesis-by-employee'),
    path('synthesis/item/<int:pk>', SynthesisByItem.as_view(), name='synthesis-by-item'),

    # cross synthesis sheet
    path('synthesis/<str:func>/<int:pk>', Synthesis.as_view(), name='synthesis'),
    
    path('payslips/<str:pk>', Payslips.as_view(), name='payslips'),
    path('payslip/<int:pk>', Payslip.as_view(), name='payslip'),
]
