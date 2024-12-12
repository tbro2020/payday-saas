from django.http import HttpResponse
from core.views import BaseView
import pandas as pd
import json

class CanvasItemsToPay(BaseView):
    headers = [{
        'matricule': None,
        
        'type d\'element': 1,
        'code': None,
        'nom': None,

        #'temps': 0,
        #'taux': 0,
        
        'montant quote part employee': 0,
        'montant quote part employeur': 0,

        'plafond de la sécurité sociale': 0,
        'montant imposable': 0,

        'est une prime': 0,
        #'est payable': 1,
    }]

    def get(self, request):
        df = pd.read_json(json.dumps(self.headers))
        response = HttpResponse(content_type='application/xlsx')
        response['Content-Disposition'] = f'attachment; filename="canvas-items-to-pay.xlsx"'.lower()

        with pd.ExcelWriter(response) as writer:
            df.to_excel(writer, sheet_name='global', index=False)
        return response

