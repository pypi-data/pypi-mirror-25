DRF_SETTINGS = {
    'exclude_apps': ['admin', 'contenttypes', 'auth', 'sessions'],
    'include_apps': [],
    'version': 1,
    'api': {
        'mixins': 'drf_scaffolding.management.core.api.mixins',
        'routers': 'drf_scaffolding.management.core.api.routers',
        'serializers': 'drf_scaffolding.management.core.api.serializers',
        'viewsets': 'drf_scaffolding.management.core.api.viewsets'
    }
}
