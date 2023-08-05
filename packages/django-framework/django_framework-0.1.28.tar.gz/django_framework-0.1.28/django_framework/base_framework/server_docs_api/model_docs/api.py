
import copy
from django_framework.django_helpers.api_helpers import BaseAPI
from django.conf.urls import RegexURLPattern, RegexURLResolver
from django.core import urlresolvers

from django_framework.django_helpers.model_helpers.model_registry import get_model, get_model_name_list
from django_framework.django_helpers.serializer_helpers.serialize_registry import get_serializer
from django_framework.django_helpers.manager_helpers.manager_registry import get_manager
from django_framework.django_helpers.meta_helpers.meta_registry import get_meta


# the easiest thing to do is to get all the models!
from django.conf import settings
class ModelDocAPI(BaseAPI):
    
    def __init__(self, request, model_name, **kwargs):
        
        kwargs['request_requires_authentication'] = False # we want to check later!
        
        super(ModelDocAPI, self).__init__(request=request, **kwargs)

        self.model_name = model_name
        
        self.Model = get_model(model_name = self.model_name)
        self.Serializer = get_serializer(self.model_name, version = self.version)
        
        if self.version == 'admin':
            pass

    def get_model_docs(self):
        
        model_fields = self.Model._meta.get_fields(include_parents=True, include_hidden=False)
        
        data = {}
        for field in model_fields:
            if field.name in self.Serializer.Meta.fields:
                data[field.name] = field.get_internal_type()
        
        self.response = data
    
    
    def get_response(self):
        '''Override BaseAPI version of get_response to get autoformatting of data'''
        return self.format_data(data = self.response)
    
    def format_data(self, data):

        return dict(data=data, meta_data = {'type' : 'docs', "total_query_results": 1, 'model' : self.model_name})
    
    
    def check_allowed_method(self):
        pass
    