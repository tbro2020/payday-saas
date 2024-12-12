from core.models import Menu, UserContentTypeApprover, Approval
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.apps import apps

def base(request):
    if not request.user.is_authenticated: return {'organization': request.organization}
    modules = Menu.objects.filter().order_by('created_at')
    
    menu = [{
        'title': module.name,
        'href': f'#{module.name}',
        'icon': f'bi-{module.icon}',
        'class': 'active',
        'children': [{
            'title': child.name,
            'href': reverse_lazy('core:list', kwargs={'app': child.app_label, 'model': child.model}),
            'permission': f'{child.app_label}.view_{child.model}'
        } for child in module.children.all() if request.user.has_perm(f'{child.app_label}.view_{child.model}')]
    } for module in modules]
    
    menu.insert(0, dict({
        'title': _('Tableau de bord'),
        'href': reverse_lazy('core:home'),
        'icon': 'bi-grid-fill',
        'forced': True
    }))

    menu.insert(1, dict({
        'title': _('Action requise'),
        'href': reverse_lazy('core:action-required'),
        'icon': 'bi-lightning-fill',
        'forced': True,
        'badge': action_required(request).get('count', 0)
    }))

    menu.insert(2, dict({
        'title': _('Notifications'),
        'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'notification'})+'?viewed=false',
        'icon': 'bi-bell',
        'forced': True,
        'badge': notifications(request).get('count', 0)
    }))
    
    menu.insert(len(menu), dict({
        'title': _('Paramètres'),
        'href': '#',
        'icon': 'bi-gear-fill',
        'children': [item for item in [{
            'title': _('Menus'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'menu'}),
            'permission': 'core.view_menu'
        }, {
            'title': _('Importeur'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'importer'}),
            'permission': 'core.view_menu'
        }, {
            'title': _('Modèle de document'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'template'}),
            'permission': 'core.view_template'
        }, {
            'title': _('Widget'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'widget'}),
            'permission': 'core.view_widget'
        }, {
            'title': _('Préférences'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'preference'}),
            'permission': 'core.view_preference'
        }, {
            'title': _('Utilisateurs'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'user'}),
            'permission': 'core.view_user'
        }, {
            'title': _('Autorisations des groupes'),
            'href': reverse_lazy('core:list', kwargs={'app': 'auth', 'model': 'group'}),
            'permission': 'auth.view_group'
        }, {
            'title': _('Approbateur de type de contenu'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'contenttypeapprover'}),
            'permission': 'core.view_contenttypeapprover'
        }, {
            'title': _('Job'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'job'}),
            'permission': 'core.view_job'
        }, {
            'title': _('Journal d\'activité'),
            'href': reverse_lazy('core:activity-log'),
            'permission': 'admin.view_logentry'
        }] if request.user.has_perm(item.get('permission'))]
    }))
    
    menu.append(dict({
        'title': _('Profil'),
        'href': '#',
        'icon': 'bi-person-lines-fill',
        'children': [{
            'title': _('Modifier le mot de passe'),
            'href': reverse_lazy('core:password-change')
        }, {
            'title': _('Se déconnecter'),
            'href': reverse_lazy('logout')
        }]
    }))
    return {'menus': menu, 'organization': request.organization}

def notifications(request):
    if not request.user.is_authenticated: return {}
    model = apps.get_model('core', 'notification')
    notifications = model.objects.filter(**{
        '_to': request.user,
        'viewed': False
    }).count()
    return {'count': notifications}

def action_required(request):
    if not request.user.is_authenticated: return {}
    
    fields = [f'content_type_approver__content_type__{field}' for field in ['app_label', 'model']]
    approvers = UserContentTypeApprover.objects.filter(user=request.user)
    approvers = approvers.values(*fields).distinct()

    # search for all objects that are not approved
    action_required_count = 0
    for approver in approvers:
        app, model_name = approver.values()
        model = apps.get_model(app_label=app, model_name=model_name)
        ids = list(map(str, model.objects.values_list('id', flat=True)))

        # remove ids that have already been approved
        approvals = Approval.objects.filter(**{
            'content_type__model': model_name,
            'content_type__app_label': app,
            'created_by': request.user,
            'object_pk__in': ids,
        }).values_list('object_pk', flat=True)
        approvals = list(approvals)
        action_required_count += len(set(ids) - set(approvals))
    
    # return the count of action required
    return {'count': action_required_count}