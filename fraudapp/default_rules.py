from .models import  MatcherRulesConfig

def default_rules():

    if not MatcherRulesConfig.objects.filter(rule_tag = 'same_id_number'):
        rule = MatcherRulesConfig()
        rule.rule_name = "same id number with another person"
        rule.rule_tag = "same_id_number"
        rule.rule_description = "applied only if the person has same id number with another"
        rule.rule_value = 100
        rule.save()

    if not MatcherRulesConfig.objects.filter(rule_tag = 'same_last_name'):
        rule = MatcherRulesConfig()
        rule.rule_name = "same last name with another person"
        rule.rule_tag = "same_last_name"
        rule.rule_description = "applied only if the person has same last name with another"
        rule.rule_value = 40
        rule.save()
        
    if not MatcherRulesConfig.objects.filter(rule_tag = 'same_first_name'):
        rule = MatcherRulesConfig()
        rule.rule_name = "same first name with another person"
        rule.rule_tag = "same_first_name"
        rule.rule_description = "applied only if the person has same first name with another"
        rule.rule_value = 20
        rule.save()

    if not MatcherRulesConfig.objects.filter(rule_tag = 'similar_first_name'):
        rule = MatcherRulesConfig()
        rule.rule_name = "similar first name with another person"
        rule.rule_tag = "similar_first_name"
        rule.rule_description = "applied only if the person has similar first name with another"
        rule.rule_value = 15
        rule.save()
    
    if not MatcherRulesConfig.objects.filter(rule_tag = 'same_date_of_birth'):
        rule = MatcherRulesConfig()
        rule.rule_name = "same date of birth with another person"
        rule.rule_tag = "same_date_of_birth"
        rule.rule_description = "applied only if the person has same date of birth with another"
        rule.rule_value = 40
        rule.save()