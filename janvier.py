from employee.models import *
from payroll.models import *
import json

from django.db.models import Sum
from datetime import datetime, timedelta

items = open('paie_janvier.json', mode='rb')
items = json.loads(items.read())

payslips = {}

for item in items:
    registration_number = item.get('MATRICULE', None)
    if not registration_number: continue
    if registration_number not in payslips:
        payslips[registration_number] = []
    payslips[registration_number].append(item)

"""
not_found = []
found = []

# first update the user data
for registration_number, items in payslips.items():
    obj = Employee.objects.filter(registration_number=str(registration_number)).first()
    if not obj:
        not_found.append(registration_number)
        continue
    found.append(registration_number)
    item = items[0]
    # print(item)
    if not item: continue
    obj.social_security_number = item['INSS'] if 'INSS' in item else obj.social_security_number
    obj.payment_account = item['COMPTE_BANCAIRE'] or obj.payment_account

    # status
    status = 'EN SERVICE' if item['ACTIVITE'] == 'ACTIF' else item['ACTIVITE']
    status, created = Status.objects.get_or_create(name=status)
    if not created: print('created status', obj, status)
    obj.status = status

    # grade
    grade = item['GRADE']
    grade, created = Grade.objects.get_or_create(name=grade)
    if not created: print('created grade' , obj, grade)
    obj.grade = grade

    # bank
    payer = item['CODE_BANQUE']
    payer, created = Payer.objects.get_or_create(name=payer)
    #if not created: print('created payer' , obj, payer)
    obj.payer_name = payer

    obj.metadata.update({
        k:v
        for k, v in item.items()
        if k not in ['PERIODE', 'LIB_SALAIRE', 'TAUX', 
            'MONTANT', 'SOLDE', 'TOT_GENERAL', 'TOTAL_RETENUE', 'NET']
    })
    obj.save()
    print(registration_number, obj)

#print(not_found)
print(found)
"""

from random import randint

item_code = {
    'RENTE PENSION': '1110', 
    'IND.ASSIDUITE': '3620', 
    'AMEUBLEMENT': '3260', 
    'SAL. DE BASE': '1010', 
    'COMP.REM/A.f.': '3820', 
    'PR.ANCIENNETE': '1000', 
    'IND.EXPLOITAT.': '3670', 
    'IND.FORF. CF,PM,CN & PTF': '3810', 
    'LOGEMENT': '3530', 
    'IND CONJONCTURE': '3640', 
    'IND.VIE CHERE': '3970', 
    'PROVISION TRANS.': '3660', 
    'IND.TRANS.BUS': '3570', 
    'IND.FONCTION.': '3800', 
    'REC.RENTE.PENS.': '1112', 
    'QP.PR.FONCT.': '2804', 
    'PR.FONCTION    1': '2800', 
    'FRAIS REPRESENT.': '3040', 
    'RBT.ELECTR.': '4603', 
    'ALL.FAMILIALE': '2010', 
    'RBT.EAU.': '4593', 
    'PR.RESPONSAB.': '2810', 
    'FRAIS DOMEST.': '3100', 
    'IND.K.M.': '3540', 
    'RECON.DETTE.': '4340', 
    'PRIME DE DIPLOME': '2160', 
    'REC.DEB.EAU': '3702', 
    'PRIME CONDUCTEUR': '3940', 
    'REC.LOGEMENT': '3532', 'AVANCE FEMME.': '4290', 'FORFAIT POLICE': '2840', 
    'ABSENCE': '4680', 'REC.PRET PERS.DI': '4480', 'RETENUES DIVERSES $': '4810', 
    'REC.FACTURE': '4360', 'REC.PRET.PERS.CA': '4490', 'REC. 1/3 SALAIRE': '1082', 
    'PECULE CONGE': '3650', 'REC.CLO.COMPTE ACTUA': '1072', 'HEURES SHIFT': '2020', 
    'SALAIRE IMPAYE': '3150', 'RAP.TRANS.BUS': '3571', 'REC.PRET PERS.CADR $': '4530', 
    'REC.IND.FONCT': '3802', 'REC.FR.DOMEST.': '3102', 'REC.IND VIE CHERE': '3972', 
    'REC IND.KM': '3542', 'REC.PROV.TRANS': '3662', 'REC.EAU.': '4590', 'REC.IND.CONJONC.': '3642', 
    'REC.ELECTRICITE': '4600', 'REC.IND.DECES': '3362', 'REC.IND.EXPLOIT. DIR': '3672', 'REC.SAL. BASE': '1012', 
    'REC.IND.ASTREINTE': '3952', 'REC.PRET PER. MAIT $': '4540', 'REC.PRET PERS.MA': '4500', 'REC.IND.HOTEL': '3012', 
    'REC.AV.CRED.VEH. $': '4210', 'REC.PR.RESPONS.': '2812', 'IND.TRACTION.': '3890', 'DETTE ONATRA': '4720', 
    'IND.DE GARDE': '3850', 'PR.30ANS.SERVIC': '3170', 'MISE A PIED': '4690', 'REC.PRET PERS $': '4520', 
    'REC.FR.FUNER.': '3052', 'REC.FRS.MANUTE. $': '4350', 'REC.PRET PERS.EX': '4510', 'REC.IND.FORF.CF&': '3812', 
    'REC.REM.A PAYER': '2822', 'PRIME DE RISQUE': '2790', 'PRIME INCOMMODITE': '3990'}

def get_item_code(item):
    if item in item_code: return item_code[item]
    item_code[item] = randint(4000, 5000)
    return item_code[item]

def five_percent_to_eight_percent(value):
    value = abs(value)
    return (value + ((value/5) * 3)) * -1

january = datetime(2024, 1, 1)

payroll, created = Payroll.objects.get_or_create(**{
    'name': 'Janvier 2024',
    'start_dt': january,
    'end_dt': january + timedelta(days=30),
})

print(len(payslips))
for emp, items in payslips.items():
    emp = Employee.objects.filter(registration_number=str(emp)).first()
    if not emp: continue
    payslip, created = Payslip.objects.get_or_create(**{
        'employee': emp,
        'payroll': payroll
    })

    items = [ItemPaid(**{
        'type_of_item': 1 if item['MONTANT'] > 0 else -1,
        'code': get_item_code(item['LIB_SALAIRE']),
        'name': item['LIB_SALAIRE'],
        'amount_qp_employer': five_percent_to_eight_percent(item['MONTANT']) if item['LIB_SALAIRE'] == 'RETENUE INSS' else 0,
        'amount_qp_employee': item['MONTANT'],
        'payslip': payslip,
        'metadata': item
    }) for item in items]

    ItemPaid.objects.bulk_create(items)

    items_paid = payslip.itempaid_set.filter(is_payable=True)
    payslip.gross = round(items_paid.aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)
    payslip.net = round(items_paid.aggregate(amount=Sum('amount_qp_employee')).get('amount', 0), 2)

    payslip.social_security_threshold = round(items_paid.aggregate(amount=Sum('social_security_amount')).get('amount', 0), 2)
    payslip.taxable_gross = round(items_paid.aggregate(amount=Sum('taxable_amount')).get('amount', 0), 2)
    payslip.save()
    print(payslip)

overall_net = payroll.payslip_set.all().aggregate(amount=Sum('net')).get('amount', 0)
payroll.overall_net = round(overall_net, 2) if overall_net else 0

payroll.status = PayrollStatus.SUCCESS
payroll.save()