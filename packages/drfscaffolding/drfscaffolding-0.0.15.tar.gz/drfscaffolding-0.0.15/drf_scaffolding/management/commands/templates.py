# -*- coding: utf-8 -*-
API_TEMPLATE = '''# -*- coding: utf-8 -*-
from app.{{app_name}}.serializers import {{model.name|lower}} as serializers
from app.{{app_name}}.models import {{model.name}}

from soft_drf.api import mixins
from soft_drf.api.viewsets import GenericViewSet


class {{model.name}}ViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.PartialUpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    serializer_class = serializers.{{model.name}}Serializer
    list_serializer_class = serializers.{{model.name}}Serializer
    retrieve_serializer_class = serializers.{{model.name}}Serializer
    create_serializer_class = serializers.{{model.name}}Serializer
    update_serializer_class = serializers.{{model.name}}Serializer

    permission_classes = []  # put your custom permissions here

    def get_queryset(self, *args, **kwargs):
        queryset = {{model.name}}.objects.all()
        return queryset
'''

ROUTE_TEMPLATE = '''# -*- coding: utf-8 -*-
from .viewsets import (
    {%for model in models%}{{model.name|lower}},{% if not forloop.last %}\n    {%endif%}{%endfor%}
)

from soft_drf.routing.v{{api_version}}.routers import router


{% for model in models %}router.register(
    r"{{model.name|lower}}s",
    {{model.name|lower}}.{{model.name}}ViewSet,
    base_name="{{model.name|lower}}s",
){% if not forloop.last %}\n\n{%endif%}{% endfor %}
'''

SERIALIZER_TEMPLATE = '''# -*- coding: utf-8 -*-
from app.{{app_name}}.models import {{model.name}}

from soft_drf.api.serializers import ModelSerializer


class {{model.name}}Serializer(ModelSerializer):

    class Meta:
        model = {{model.name}}
        fields = ({%if model.fields%}{%for field in model.fields%}
            '{{field}}',{%endfor%}{%else%}
            'id',{%endif%}
        )
'''
