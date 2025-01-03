from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from core.models import Menu
from django.apps import apps

def base(request):
    if not request.user.is_authenticated: return {'organization': request.organization}
    modules = Menu.objects.filter().order_by('created_at')
    
    menu = [{
        'class': 'module active',
        'title': module.name,
        'href': f'#{module.name}',
        'icon': f'bi-{module.icon}',
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
        'forced': True,
        'description': _('Tous vos widgets en un seul endroit, des statistiques, des graphiques et bien plus encore.')
    }))

    menu.insert(1, dict({
        'title': _('Action requise'),
        'href': reverse_lazy('core:action-required'),
        'icon': 'bi-lightning-fill',
        'forced': True,
        'badge': action_required(request).get('count', 0),
        'description': _('Les actions qui nécessitent votre attention.')
    }))

    menu.insert(2, dict({
        'title': _('Notifications'),
        'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'notification'})+'?viewed=False',
        'icon': 'bi-bell',
        'forced': True,
        'badge': notifications(request).get('count', 0),
        'description': _('Les notifications qui vous sont destinées.')
    }))
    
    menu.insert(len(menu), dict({
        'class': 'active',
        'title': _('Paramètres'),
        'href': '#',
        'icon': 'bi-gear-fill',
        'description': _('Paramètres de votre organisation.'),
        'children': [item for item in [{
            'title': _('Menus'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'menu'}),
            'permission': 'core.view_menu',
            'description': _('Faite la disposition de vos menus.')
        }, {
            'title': _('Importeur'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'importer'}),
            'permission': 'core.view_menu',
            'description': _('Importez vos données en masse.')
        }, {
            'title': _('Modèle de document'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'template'}),
            'permission': 'core.view_template',
            'description': _('Créez des modèles de document reutilisable pour vos models.')
        }, {
            'title': _('Widget'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'widget'}),
            'permission': 'core.view_widget',
            'description': _('Créez des widgets pour votre tableau de bord, ainsi que listing.')
        }, {
            'title': _('Préférences'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'preference'}),
            'permission': 'core.view_preference',
            'description': _('Définissez vos préférences pour une meilleure expérience.')
        }, {
            'title': _('Utilisateurs'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'user'}),
            'permission': 'core.view_user',
            'description': _('Gérez les utilisateurs de votre organisation.')
        }, {
            'title': _('Roles'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'role'}),
            'permission': 'auth.view_group',
            'description': _('Gérez les roles de votre organisation.')
        }, {
            'title': _('Job'),
            'href': reverse_lazy('core:list', kwargs={'app': 'core', 'model': 'job'}),
            'permission': 'core.view_job',
            'description': _('Mettez en place des tâches automatisées.')
        }, {
            'title': _('Journal d\'activité'),
            'href': reverse_lazy('core:activity-log'),
            'permission': 'admin.view_logentry',
            'description': _('Consultez l\'historique des activités.')
        }] if request.user.is_superuser or request.user.is_staff] # if request.user.has_perm(item.get('permission'))]
    }))
    
    menu.append(dict({
        'class': 'active',
        'title': _('Profil'),
        'href': '#',
        'icon': 'bi-person-lines-fill',
        'children': [{
            'title': _('Modifier le mot de passe'),
            'href': reverse_lazy('core:password-change'),
            'description': _('Changer votre mot de passe.')
        }, {
            'title': _('Se déconnecter'),
            'href': reverse_lazy('core:logout'),
            'description': _('Déconnectez-vous de votre compte.')
        }]
    }))
    return {'menus': menu, 'organization': request.organization}

def notifications(request):
    return {'count': 0}
    if not request.user.is_authenticated: return {}
    model = apps.get_model('core', 'notification')
    notifications = model.objects.filter(**{
        '_to': request.user,
        'viewed': False
    }).count()
    return {'count': notifications}

def action_required(request):
    return {'count': 0}