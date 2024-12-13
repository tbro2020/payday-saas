from django.urls import path
from payroll.views import *

app_name = 'payroll'

urlpatterns = [
    path('canvas-items-to-pay', CanvasItemsToPay.as_view(), name='canvas-items-to-pay'),
    path('canvas', Canvas.as_view(), name='canvas'),

    path('sheet/<int:pk>', SheetSummary.as_view(), name='sheet'),
    path('listing/<int:pk>', Listing.as_view(), name='listing'),
    
    # cross synthesis sheet
    path('synthesis/<str:func>/<int:pk>', Synthesis.as_view(), name='synthesis'),
    
    path('payslips/<str:pk>', Payslips.as_view(), name='payslips'),
    path('payslip/<int:pk>', Payslip.as_view(), name='payslip'),
    path('slips', Slips.as_view(), name='slips'),
]
