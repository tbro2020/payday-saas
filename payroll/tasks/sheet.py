from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
#from notifications.signals import notify
from celery import shared_task


from django.utils.text import slugify
from payroll.models import *
from core.models import *

import pandas as pd
import json
import io

@shared_task
def sheet(payroll, actor, group_by=None):
    payroll = get_object_or_404(Payroll, pk=payroll) if not isinstance(payroll, Payroll) else payroll
    
    output = io.BytesIO()
    df = pd.read_json(json.dumps(payroll.sheet()))
    df = df.groupby(group_by) if group_by else df

    with pd.ExcelWriter(output) as writer:
        [group.to_excel(writer, sheet_name=slugify(str(row)), index=False) for row, group in df] if group_by else df.to_excel(writer, index=False)

    output.seek(0)
    fs = FileSystemStorage()
    group_by = group_by if group_by else 'global'
    filename = fs.save(f'sheet_{group_by}.xlsx', output)
    
    actor = get_object_or_404(User, pk=actor)
    #notify.send(actor, recipient=actor, verb='Your export is ready! Click here to download', url=fs.url(filename))