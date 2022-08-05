from django import forms
from datetime import date
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator

# import Models
from .models import (uPillar_Survey,
                     uEDM_Observation)

from baseline_calibration.models import Uncertainty_Budget
from instruments.models import (EDM_Inst, 
                                Prism_Inst, 
                                Mets_Inst, 
                                DigitalLevel, 
                                Staff)
from calibrationsites.models import (CalibrationSite, 
                                     Pillar)

# make your forms
class uPillarSurveyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       user = kwargs.pop('user', None)                             
       super(uPillarSurveyForm, self).__init__(*args, **kwargs)
       self.fields['edm'].queryset = EDM_Inst.objects.all()
       self.fields['prism'].queryset = Prism_Inst.objects.all()
       self.fields['thermometer'].queryset = Mets_Inst.objects.filter(
           mets_specs__mets_model__inst_type = 'thermo')
       self.fields['barometer'].queryset = Mets_Inst.objects.filter(
           mets_specs__mets_model__inst_type = 'baro')
       self.fields['hygrometer'].queryset = Mets_Inst.objects.filter(
           mets_specs__mets_model__inst_type = 'hygro')
       self.fields['uncertainty_budget'].queryset = Uncertainty_Budget.objects.all()
          
   
    class Meta:
        model = uPillar_Survey
        fields = '__all__'
        exclude = ('uploaded_on', 'modified_on')       
        widgets = {
            'calibrated_baseline': forms.Select(attrs={'class': 'page0'}),
            'computation_date': forms.DateInput(format=('%d-%m-%Y'), 
                                                attrs={'class': 'page0'}),
            'survey_date': forms.DateInput(format=('%d-%m-%Y'),
                                           attrs={'class': 'page0'}),
            'observer': forms.TextInput(attrs={'class': 'page0'}),
            'weather': forms.Select(attrs={'class': 'page0'}),
            'job_number': forms.TextInput(attrs={'class': 'page0'}),
             
            'edm': forms.Select(attrs={'class': 'page1'}),
            'prism': forms.Select(attrs={'class': 'page1'}),
            'thermometer': forms.Select(attrs={'class': 'page1'}),
            'barometer': forms.Select(attrs={'class': 'page1'}),
            'hygrometer': forms.Select(attrs={'class': 'page1'}),  
            'mets_applied': forms.CheckboxInput(attrs={'class': 'page1'}),
            'thermo_calib_applied': forms.CheckboxInput(attrs={'class': 'page'}),
            'baro_calib_applied': forms.CheckboxInput(attrs={'class': 'page'}),
            'hygro_calib_applied': forms.CheckboxInput(attrs={'class': 'page0'}),
            
            'uncertainty_budget': forms.Select(attrs={'class': 'page1'}),
             }


    def clean_survey_date(self):
        survey_date = self.cleaned_data['survey_date']
        if survey_date > date.today():
            raise forms.ValidationError("The survey date cannot be in the future!")
        return survey_date
    
    
    def computation_date_date(self):
        computation_date = self.cleaned_data['computation_date']
        if computation_date > date.today():
            raise forms.ValidationError("The computation date cannot be in the future!")
        return computation_date


# class CalibrateEdmForm2(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        user = kwargs.pop('user', None)                             
#        super(CalibrateEdmForm2, self).__init__(*args, **kwargs)
#        self.fields['edm'].queryset = EDM_Inst.objects.all()
#        self.fields['prism'].queryset = Prism_Inst.objects.all()
#        self.fields['thermometer'].queryset = Mets_Inst.objects.filter(mets_specs__mets_model__inst_type = 'thermo')
#        self.fields['barometer'].queryset = Mets_Inst.objects.filter(mets_specs__mets_model__inst_type = 'baro')
#        self.fields['hygrometer'].queryset = Mets_Inst.objects.filter(mets_specs__mets_model__inst_type = 'hygro')
          
#    class Meta:
#        model = uPillar_Survey
#        fields = ['edm', 'prism',
#                  'thermometer', 
#                  'barometer', 
#                  'hygrometer', 
#                  'mets_applied',
#                  'thermo_calib_applied', 
#                  'baro_calib_applied', 
#                  'hygro_calib_applied',     
#                  ]
#        widgets = {
#            'edm': forms.Select(attrs={'required': 'true'}),
#            'prism': forms.Select(attrs={'required': 'true'}),
#            'thermometer': forms.Select(attrs={'required': 'true'}),
#            'barometer': forms.Select(attrs={'required': 'true'}),
#            'hygrometer': forms.Select(attrs={'required': 'false'}),   
#            'mets_applied': forms.CheckboxInput(), 
#            'thermo_calib_applied': forms.CheckboxInput(), 
#            'baro_calib_applied': forms.CheckboxInput(), 
#            'hygro_calib_applied': forms.CheckboxInput(),
#             }


class CalibrateEdmForm3(forms.ModelForm):
   def __init__(self, *args, **kwargs):
       user = kwargs.pop('user', None)                             
       super(CalibrateEdmForm3, self).__init__(*args, **kwargs)
       self.fields['uncertainty_budget'].queryset = Uncertainty_Budget.objects.all()
   
   class Meta:
       model = uPillar_Survey
       fields = ['uncertainty_budget'
                 ]
       widgets = {
           'uncertainty_budget': forms.Select(attrs={'required': 'true'}),
            }
   outlier_criterion = forms.FloatField(
                             widget=forms.NumberInput(
                                   attrs={'placeholder':'Enter number of standard deviations for outlier detection','required': 'true'}), 
                                   validators=[
                                           MaxValueValidator(5.0),
                                           MinValueValidator(0)
                                           ],
                                   label = "Rejection Criteria for outlier detection")
   Scanned_field_notes = forms.FileField(widget=forms.FileInput(attrs={'accept' : '.jpg, .pdf'}),
   	   	   	   	   	   	   	   	   	   	   	   	   	   	   	   	   	   	required = False)
   
   edm_file = forms.FileField(widget=forms.FileInput(attrs={'accept' : '.csv, .asc'}), label = 'EDM File (*.csv)')

class CalibrateEdmForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CalibrateEdmForm, self).__init__(*args, **kwargs)
        if user.is_staff==True:
            self.fields['edm'].queryset = EDM_Inst.objects.all()
            self.fields['prism'].queryset = Prism_Inst.objects.all()
            self.fields['thermometer'].queryset = Mets_Inst.objects.filter(
                mets_specs__mets_model__inst_type = 'thermo')
            self.fields['barometer'].queryset = Mets_Inst.objects.filter(
                mets_specs__mets_model__inst_type = 'baro')
            self.fields['hygrometer'].queryset = Mets_Inst.objects.filter(
                mets_specs__mets_model__inst_type = 'hygro')
        else:
            self.fields['edm'].queryset = EDM_Inst.objects.filter(
                edm_specs__edm_owner = user.company)
            self.fields['prism'].queryset = Prism_Inst.objects.filter(
                prism_specs__prism_owner = user.company)
            self.fields['thermometer'].queryset = Mets_Inst.objects.filter(
                mets_specs__mets_model__inst_type = 'thermo',
                mets_specs__mets_owner = user.company)
            self.fields['barometer'].queryset = Mets_Inst.objects.filter(
                mets_specs__mets_model__inst_type = 'baro',
                mets_specs__mets_owner = user.company)
            self.fields['hygrometer'].queryset = Mets_Inst.objects.filter(
                mets_specs__mets_model__inst_type = 'hygro',
                mets_specs__mets_owner = user.company)
        self.fields['uncertainty_budget'].queryset = Uncertainty_Budget.objects.filter(
            Q(company = user.company) | 
            Q(name = 'Default', company__company_name = 'Landgate'))
            
    class Meta:
        model = uPillar_Survey
        fields = '__all__'
        exclude = ('uploaded_on', 'modified_on')
        widgets = {
           'calibrated_baseline': forms.Select(attrs={'class': 'page0'}),
           'computation_date': forms.DateInput(format=('%d-%m-%Y'),
               attrs={'type':'date', 'class': 'page0'}),
           'survey_date': forms.DateInput(format=('%d-%m-%Y'), 
               attrs={'type':'date', 'class': 'page0'}),
           'observer': forms.TextInput (attrs={'class': 'page0'}),	
           'weather': forms.Select(attrs={'class': 'page0'}),
           'job_number': forms.TextInput (
               attrs={'required': 'false', 'class': 'page0'}),
           
           'edm': forms.Select(attrs={'class': 'page1'}),
           'prism': forms.Select(attrs={'class': 'page1'}),
           'thermometer': forms.Select(attrs={'class': 'page1'}),
           'barometer': forms.Select(attrs={'class': 'page1'}),
           'hygrometer': forms.Select(attrs={'class': 'page1'}),
           'mets_applied': forms.CheckboxInput(attrs={'class': 'page1'}), 
           'thermo_calib_applied': forms.CheckboxInput(attrs={'class': 'page1'}), 
           'baro_calib_applied': forms.CheckboxInput(attrs={'class': 'page1'}), 
           'hygro_calib_applied': forms.CheckboxInput(attrs={'class': 'page1'}),
            
           'uncertainty_budget': forms.Select(attrs={'class': 'page2'}),
           'outlier_criterion': forms.NumberInput(
               attrs={'placeholder':'Enter number of standard deviations for outlier detection',
                      'class': 'page2'}), 
           'fieldnotes_upload': forms.FileInput(attrs={'accept' : '.jpg, .pdf',
                                                         'class': 'page2'})
            }
        labels = {'outlier_criterion': 'Rejection Criteria for outlier detection',
                  'fieldnotes_upload': 'Scanned Fieldnotes'}
        
    edm_file = forms.FileField(
        widget = forms.FileInput(attrs={'accept' : '.csv, .asc',
                                        'class': 'page2'}), 
        label = 'EDM File (*.csv)')
    
    def clean_survey_date(self):
        survey_date = self.cleaned_data['survey_date']
        if survey_date > date.today():
            raise forms.ValidationError("The survey date cannot be in the future!")
        return survey_date
    
    def computation_date_date(self):
        computation_date = self.cleaned_data['computation_date']
        if computation_date > date.today():
            raise forms.ValidationError("The computation date cannot be in the future!")
        return computation_date

# insert your forms
from .models import StepBySteGuideModel

class StepBySteGuideForm(forms.ModelForm):
    class Meta:
        model = StepBySteGuideModel
        fields = "__all__" 
        widgets = {
        'content': forms.TextInput(attrs={'class': 'text-area2'}),
        }