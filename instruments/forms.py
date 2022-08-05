from django import forms
from django.db.models import Q
from django.db.utils import OperationalError
# from django.core.exceptions import NON_FIELD_ERRORS
from .models import (
					InstrumentMake, 
                    InstrumentModel, 
                    Staff, 
                    DigitalLevel,
                    EDM_Inst,
                    EDM_Specification,
                    Prism_Inst,
                    Prism_Specification,
                    Mets_Inst,
                    Mets_Specification,
                    )

from accounts.models import Company, CustomUser
# Prepare forms
#############################################################################
class InstrumentMakeCreateForm(forms.ModelForm):
    class Meta:
        model = InstrumentMake
        fields = '__all__'

class InstrumentModelCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(InstrumentModelCreateForm, self).__init__(*args, **kwargs) 
        self.fields['make'].empty_label = '--- Select one ---'  

    class Meta:
        model = InstrumentModel
        fields = '__all__'
###################################################################
class InstrumentModelCreateByInstTypeForm(forms.Form):
    inst_types = (
                ( None, 'Select one of the following'),
                ('edm','Total Station EDM'),
                ('prism','Prism'),
                ('level','Digital Level'),
                ('staff','Barcoded Staff'),
                ('baro','Barometer'),
                ('thermo','Themometer'),
                ('hygro','Hygrometer'),
                ('psy','Psychrometer'))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        inst_type = kwargs.pop('inst_type')
        super(InstrumentModelCreateByInstTypeForm, self).__init__(*args, **kwargs)
        self.initial['inst_type'] = inst_type
    
    inst_type = forms.ChoiceField(widget = forms.Select(), choices = inst_types)
    try:
        obj, created = InstrumentMake.objects.get_or_create(make='OTHERS',
                                            make_abbrev= 'OTHERS')
    except OperationalError as e:
        pass
    make = forms.ModelChoiceField(empty_label='Select one of the following',
                                required=True,
                                queryset=InstrumentMake.objects.all(),
                                widget=forms.Select())

    inst_make = forms.CharField(max_length=25, min_length=4, required=False, help_text="e.g., LEICA, TRIMBLE, SOKKIA", label = 'Make (New)')
    inst_abbrev = forms.CharField(max_length=4, min_length=3, required=False, help_text="e.g., LEI, TRIM, SOKK",  label = 'Abbreviation (New)')
    model = forms.CharField(max_length=25, min_length=3, required=True, help_text="e.g., LS15, DNA03, TS30, S9, SX12, GT-1200/600", label = 'Model (new)')
##############################################################################
class DigitalLevelCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DigitalLevelCreateForm, self).__init__(*args, **kwargs)   
        self.base_fields['level_owner'].initial = user.company
        if not user.is_staff:
            self.fields['level_owner'].disabled = True
        self.fields['level_model'].empty_label = '--- Select one ---'

        # self.fields['level_owner'].queryset = Company.objects.exclude(company_abbrev__iexact='OTH')
        self.fields['level_number'].widget.attrs['placeholder'] = 'Level number, e.g., Serial number'

    level_owner = forms.ModelChoiceField(empty_label='Choose a firm/company',
                                    queryset=Company.objects.exclude(company_abbrev='OTH'),
                                    widget=forms.Select())
    class Meta:
        model = DigitalLevel
        fields = ('level_model', 'level_owner', 'level_number',)
        # exclude = ('level_model',)
#############################################################################
class StaffCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(StaffCreateForm, self).__init__(*args, **kwargs) 
        if not user.is_staff:
            self.fields['staff_owner'].queryset = Company.objects.filter(company_name=user.company.company_name)
        
        self.fields['staff_model'].empty_label = '--- Select one ---'
        self.fields['staff_owner'].empty_label = '--- Select one ---'

    staff_owner = forms.ModelChoiceField(#empty_label='--- Select one ---',
                                    queryset=Company.objects.exclude(company_abbrev='OTH'),
                                    widget=forms.Select())

    class Meta:
        model = Staff
        fields = '__all__'       
    calibrated = forms.BooleanField(required=False, label = "Is Calibrated", help_text = "Does it have a previous calibration record?")
##############################################################################
class EDM_InstForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EDM_InstForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['edm_custodian'].queryset = CustomUser.objects.filter(company__company_name = user.company.company_name) 
        self.fields['edm_custodian'].empty_label = '--- Select one ---'
        self.fields['edm_specs'].empty_label = '--- Select one ---'

    class Meta:
        model = EDM_Inst
        fields = '__all__'
        exclude = ('created_on', 'modified_on')
        widgets = {
            'photo' : forms.FileInput(attrs={'accept' : '.pdf, .jpg, .jpeg, .png, .tif','required': 'true'}),            
        }
        
class EDM_SpecificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EDM_SpecificationForm, self).__init__(*args, **kwargs) 
        self.initial['edm_owner'] = user.company
        self.base_fields['unit_manu_unc_const'].initial = 'mm'
        self.base_fields['unit_manu_unc_ppm'].initial = 'ppm'
        self.base_fields['unit_freq'].initial = 'mHz'
        self.base_fields['unit_unit_length'].initial = 'm'
        self.base_fields['unit_carrier_wave'].initial = 'nm'
        self.base_fields['unit_measurement_inc'].initial = 'mm'
        if not user.is_staff:
            self.fields['edm_owner'].disabled = True
        self.fields['edm_model'].empty_label = '--- Select one ---'

    class Meta:
        model = EDM_Specification
        fields = '__all__'
        exclude = ('created_on', 'modified_on')
    
    length_units = (
            ('nm','nm'),
            ('mm','mm'),
            ('m','m'),)
    freq_units = (
            ('Hz','Hz'),
            ('mHz','mHz'),)
    scalar_units = (
            ('1:x','1:x'),
            ('ppm','ppm'),)
        
    unit_manu_unc_const = forms.CharField(
                                    widget=forms.Select(choices=length_units))

    unit_manu_unc_ppm = forms.CharField(widget=forms.Select(choices=scalar_units))

    unit_freq = forms.CharField(widget=forms.Select(choices=freq_units))

    unit_unit_length = forms.CharField(
                                    widget=forms.Select(choices=length_units))

    unit_carrier_wave = forms.CharField(
                                    widget=forms.Select(choices=length_units))

    unit_measurement_inc = forms.CharField(
                                    widget=forms.Select(choices=length_units))
##############################################################################
class Prism_InstForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Prism_InstForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['prism_custodian'].queryset = CustomUser.objects.filter(company__company_name = user.company.company_name) 
        self.fields['prism_custodian'].empty_label = '--- Select one ---'
        self.fields['prism_specs'].empty_label = '--- Select one ---'

    class Meta:
        model = Prism_Inst
        fields = '__all__'
        exclude = ('created_on', 'modified_on')
        widgets = {
            'photo' : forms.FileInput(attrs={'accept' : '.pdf, .jpg, .jpeg, .png, .tif','required': 'true'}),            
        }

class Prism_SpecificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Prism_SpecificationForm, self).__init__(*args, **kwargs) 
        self.initial['prism_owner'] = user.company
        self.base_fields['unit_manu_unc_const'].initial = 'mm'
        self.base_fields['unit_manu_unc_ppm'].initial = 'ppm'
        if not user.is_staff:
            self.fields['prism_owner'].disabled = True
        self.fields['prism_model'].empty_label = '--- Select one ---'

    class Meta:
        model = Prism_Specification
        fields = '__all__'
        exclude = ('created_on', 'modified_on')
    
    length_units = (
            ('nm','nm'),
            ('mm','mm'),
            ('m','m'),)
    scalar_units = (
            ('1:x','1:x'),
            ('ppm','ppm'),)
        
    unit_manu_unc_const = forms.CharField(
                                    widget=forms.Select(choices=length_units))

    unit_manu_unc_ppm = forms.CharField(widget=forms.Select(choices=scalar_units))
##########################################################################
class Mets_InstForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Mets_InstForm, self).__init__(*args, **kwargs)
        if not user.is_staff:
            self.fields['mets_custodian'].queryset = CustomUser.objects.filter(company__company_name = user.company.company_name) 
        self.fields['mets_custodian'].empty_label = '--- Select one ---'
        self.fields['mets_specs'].empty_label = '--- Select one ---'

    class Meta:
        model = Mets_Inst
        fields = '__all__'
        exclude = ('created_on', 'modified_on')
        widgets = {
            'photo' : forms.FileInput(attrs={'accept' : '.pdf, .jpg, .jpeg, .png, .tif','required': 'true'}),            
        }

class Mets_SpecificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(Mets_SpecificationForm, self).__init__(*args, **kwargs) 
        self.initial['mets_owner'] = user.company
        self.base_fields['unit_manu_unc_const'].initial = 'mm'
        self.base_fields['unit_manu_unc_ppm'].initial = 'ppm'
        if not user.is_staff:
            self.fields['mets_owner'].disabled = True
        self.fields['mets_model'].empty_label = '--- Select one ---'

    class Meta:
        model = Mets_Specification
        fields = '__all__'
        exclude = ('created_on', 'modified_on')
    
    length_units = (
            ('nm','nm'),
            ('mm','mm'),
            ('m','m'),)
    scalar_units = (
            ('1:x','1:x'),
            ('ppm','ppm'),)
        
    unit_manu_unc_const = forms.CharField(
                                    widget=forms.Select(choices=length_units))

    unit_manu_unc_ppm = forms.CharField(widget=forms.Select(choices=scalar_units))
##########################################################################