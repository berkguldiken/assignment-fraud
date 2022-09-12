from .models import PersonData, MatcherRulesConfig, PersonDataMatcher
import difflib
from nicknames import NickNamer




class LogBuilder(list):
    def info(self, message: str):
        self.append(f'[INFO] {message}')

    def warn(self, message: str):
        self.append(f'[WARNING] {message}')

    def build(self):
        return '\n'.join(map(str, self))

class BasePipelineElement:
    def __init__(self, person_data, log_builder: LogBuilder):
        self._log_builder = log_builder
        self._match_status = 0
        self._person_data = person_data
    def run(self):
        raise NotImplementedError

class IdentificationValidator(BasePipelineElement):

    def run(self):
        _rule = MatcherRulesConfig.objects.get(rule_tag = "same_id_number")
        if self._person_data['id_number'].value == None:
            self._log_builder.info('ID Validation: NO ID is given')
        elif PersonData.objects.filter(id_number =self._person_data['id_number'].value).exists():
            self._match_status = _rule.rule_value
            self._log_builder.warn('ID Validation: Person with the same id exist')
        else:
            self._log_builder.info('ID Validation: OK. No person found with same id')
        return self._match_status
        
class FirstNameValidator(BasePipelineElement):

    def run(self):
        _rule = MatcherRulesConfig.objects.get(rule_tag = "same_first_name")

        # this checks the same name
        if PersonData.objects.filter(first_name =self._person_data['first_name'].value).exists(): # this checks the whole name similarity
            self._match_status += _rule.rule_value
            self._log_builder.warn('First Name Validation: Person with the same first name exist')

        # this checks the initials
        elif len(self._person_data['first_name'].value) <= 2 : 
            initial = self._person_data['first_name'].value[0]
            _rule = MatcherRulesConfig.objects.get(rule_tag = "similar_first_name")
            if PersonData.objects.filter(first_name__startswith=initial).exists():
                self._match_status += _rule.rule_value
                self._log_builder.warn('First Name Validation: Found a person with the same initial')
        
        #this checks typos and diminutive names
        else: 
            diff_list = [li for li in difflib.ndiff('andrew', self._person_data['first_name'].value) if li[0] != ' ']
            _rule = MatcherRulesConfig.objects.get(rule_tag = "similar_first_name")
            if len(diff_list) == 1:
                self._match_status += _rule.rule_value
                self._log_builder.warn('First Name Validation: Found a person with the same name with typo')
            
            #check if the change is only 2 characters
            elif len(diff_list) == 2: 
                for word in diff_list:
                    if '-' in word: #check if changed 2 characters are not added but one character is changed
                        self._match_status += _rule.rule_value
                        self._log_builder.warn('First Name Validation: Found a person with the same name with typo')
            
            # this checks diminutive names
            else:
                nn = NickNamer()
                nicks = nn.nicknames_of('Andrew')
                flag=True
                for f_name in PersonData.objects.values_list('first_name', flat=True):
                    nicks = nn.nicknames_of(f_name)
                    if self._person_data['first_name'].value in nicks:
                        self._match_status += _rule.rule_value  
                        flag = False
                        self._log_builder.warn('First Name Validation: Found a person with the same name using diminutive') 
                        break 
                if flag:
                    self._log_builder.info('First Name Validation: OK. No person found with same or similar first name')
        return self._match_status

# checks and matches the last name of given person
class LastNameValidator(BasePipelineElement):

    def run(self):
        _rule = MatcherRulesConfig.objects.get(rule_tag = "same_last_name")
        if PersonData.objects.filter(last_name =self._person_data['last_name'].value).exists():
            self._match_status += _rule.rule_value
            self._log_builder.warn('Last Name Validation: Person with the same last name exist')
        else:
            self._log_builder.info('Last Name Validation: OK. No person found with same last name')
        return self._match_status

# checks and matches the date of birth of given person
class DateOfBirthValidator(BasePipelineElement):
    
    def run(self):
        _rule = MatcherRulesConfig.objects.get(rule_tag = "same_date_of_birth") #gets the rule of same date of birth

        if self._person_data['date_of_birth'].value == None:
            self._log_builder.info('Date Of Birth Validation: NO date of birth is given')
        elif PersonData.objects.filter(date_of_birth =self._person_data['date_of_birth'].value).exists():
            self._match_status += _rule.rule_value
            self._log_builder.warn('Date Of Birth Validation: Person with the same date of birth exist')
        else:
            self._log_builder.info('Date Of Birth Validation: OK. No person found with same date of birth')
        return self._match_status

# Main frame for the person matching system
# this uses pipelines for 4 validation
#
class PersonMatcher:

    pipeline_classes = [
        IdentificationValidator,
        FirstNameValidator,
        LastNameValidator,
        DateOfBirthValidator,
    ]

    def __init__(self, person_data):
        self._person_data = person_data
        self._log_builder = LogBuilder()
        self._match_status = 0
        self._person_matcher = PersonDataMatcher()

    def _finalize(self):
        log = self._log_builder.build()
        self._person_matcher.log = log
        self._person_matcher.match_status = self._match_status
        self._person_matcher.first_name = self._person_data['first_name'].value
        self._person_matcher.last_name = self._person_data['last_name'].value
        self._person_matcher.date_of_birth = self._person_data['date_of_birth'].value
        self._person_matcher.id_number = self._person_data['id_number'].value
        self._person_matcher.save()

    def run(self):

        for cls in self.pipeline_classes:
            element = cls(self._person_data, self._log_builder)
            try:
                self._match_status += element.run()

            except Exception as e:
                self._log_builder.warn(f'During execution {element.__class__.__name__} error occured: {e}')

            if element._match_status >=100:

                break

        self._log_builder.info("DONE")
        self._finalize()
        return self._match_status

        