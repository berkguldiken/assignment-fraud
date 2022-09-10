from django.db import models
from datetime import date


class PersonData(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True,null=True)
    id_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.first_name +' '+ self.last_name


class PersonDataMatcher(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(blank=True,null=True)
    id_number = models.IntegerField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    match_status = models.IntegerField(default = 0)
    log = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.first_name +' '+ self.last_name

class MatcherRulesConfig(models.Model):
    rule_name = models.TextField()
    rule_tag = models.CharField(max_length=50,unique=True)
    rule_description = models.TextField()
    rule_value = models.IntegerField()

    def __str__(self):
        return self.rule_name