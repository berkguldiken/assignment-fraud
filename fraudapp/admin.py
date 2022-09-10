
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin
#from .models import User
from . import models



#admin.site.register(models.MatcherRulesConfig)

@admin.register(models.MatcherRulesConfig)
class MatcherRulesConfigAdmin(admin.ModelAdmin):
    list_display = ('rule_name','rule_value')

admin.site.register(models.PersonData)
#admin.site.register(models.PersonDataMatcher)


@admin.register(models.PersonDataMatcher)
class PersonDataMatcherAdmin(admin.ModelAdmin):
    list_display = ('details', 'first_name','last_name', 'created', 'match_status')
    fields = ('created', 'log', 'match_status', 'first_name','last_name','date_of_birth','id_number')
    readonly_fields = fields[:-1]
    list_filter = ('match_status',)
    actions = []

    @staticmethod
    def details(*_, **__):
        return 'see details'

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return super().get_readonly_fields(request, obj)
        return self.fields

    def has_delete_permission(self, request, obj=None):
        return False