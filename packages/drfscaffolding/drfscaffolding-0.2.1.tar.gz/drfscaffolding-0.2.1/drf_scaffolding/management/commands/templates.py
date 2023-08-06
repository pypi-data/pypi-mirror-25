# -*- coding: utf-8 -*-
API_TEMPLATE = '''# -*- coding: utf-8 -*-
from app.{{app_name}}.models import {{model.name}}
from app.{{app_name}}.serializers import {{model.name|lower}} as serializers

from soft_drf.api import mixins
from soft_drf.api.viewsets import GenericViewSet


class {{model.name}}ViewSet(
    GenericViewSet,{%if 'LIST' in model.methods%}\n    mixins.ListModelMixin,{%endif%}{%if 'RETRIEVE' in model.methods%}\n    mixins.RetrieveModelMixin,{%endif%}{%if 'CREATE' in model.methods%}\n    mixins.CreateModelMixin,{%endif%}{%if 'UPDATE' in model.methods%}\n    mixins.PartialUpdateModelMixin,{%endif%}{%if 'DELETE' in model.methods%}\n    mixins.DestroyModelMixin,{%endif%}
):
    serializer_class = serializers.{{model.name}}Serializer{%if 'LIST' in model.methods%}\n    list_serializer_class = serializers.{{model.name}}Serializer{%endif%}{%if 'RETRIEVE' in model.methods%}\n    retrieve_serializer_class = serializers.{{model.name}}Serializer{%endif%}{%if 'CREATE' in model.methods%}\n    create_serializer_class = serializers.{{model.name}}Serializer{%endif%}{%if 'DELETE' in model.methods%}\n    update_serializer_class = serializers.{{model.name}}Serializer{%endif%}

    permission_classes = []  # put your custom permissions here

    def get_queryset(self, *args, **kwargs):
        queryset = {{model.name}}.objects.all()
        return queryset
'''

ROUTE_TEMPLATE = '''# -*- coding: utf-8 -*-
from soft_drf.routing.v{{api_version}}.routers import router

from .viewsets import (
    {%for model in models%}{{model.name|lower}},{% if not forloop.last %}\n    {%endif%}{%endfor%}
)


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


FORM_TEMPLATE = '''from app.{{app_name}}.models import {{model.name}}

from django import forms


class {{model.name}}AdminForm(forms.ModelForm):
    class Meta:
        model = {{model.name}}
        fields = {%if model.fields%}[{%for field in model.fields%}
            '{{field}}',{%endfor%}
        ]{%else%}'__all__'{%endif%}
'''


ADMIN_TEMPLATE = '''{%for model in models%}from app.{{app_name}}.forms.{{model.name|lower}} import {{model.name}}AdminForm
{%endfor%}
from app.{{app_name}}.models import (
    {%for model in models%}{{model.name}},{% if not forloop.last %}\n    {%endif%}{%endfor%}
)

from django.contrib import admin


{%for model in models%}class {{model.name}}Admin(admin.ModelAdmin):
    form = {{model.name}}AdminForm
    list_display = {%if model.fields%}[{%for field in model.fields%}
        '{{field}}',{%endfor%}
    ]{%else%}'__all__'{%endif%}

    search_fields = {%if model.fields%}[{%for field in model.fields%}
        '{{field}}',{%endfor%}
    ]{%else%}'__all__'{%endif%}{% if not forloop.last %}\n\n\n{%else%}\n{%endif%}{%endfor%}
{%for model in models%}
admin.site.register({{model.name}}, {{model.name}}Admin){%endfor%}
'''
