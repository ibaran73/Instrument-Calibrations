from django.db import models
from django.db.models import Q
from datetime import date
import uuid
from django.core.validators import RegexValidator
# Import models
from accounts.models import CustomUser
from calibrationsites.models import CalibrationSite
from instruments.models import (
                            Staff,
                            DigitalLevel,
                            )
########################################################################
def get_upload_to_calibreport(instance, filename):
    filename = filename.split('\\')[-1]
    obs_date = instance.calibration_date.strftime('%Y%m%d')
    return 'RangeCalibration/%s/%s/%s/Report/%s' % (instance.site_id.state.statecode, instance.site_id.site_name, obs_date, instance.inst_staff.staff_number + '-' +  filename)

def get_upload_to_fieldfile(instance, filename):
    filename = filename.split('\\')[-1]
    obs_date = instance.calibration_date.strftime('%Y%m%d')
    return 'RangeCalibration/%s/%s/%s/FieldData/%s' % (instance.site_id.state.statecode, instance.site_id.site_name, obs_date, instance.inst_staff.staff_number + '-' +  filename)

def get_upload_to_fieldbook(instance, filename):
    filename = filename.split('\\')[-1]
    obs_date = instance.calibration_date.strftime('%Y%m%d')
    return 'RangeCalibration/%s/%s/%s/FieldBook/%s' % (instance.site_id.state.statecode, instance.site_id.site_name, obs_date, instance.inst_staff.staff_number + '-' +  filename)

# Create your models here.
class RangeCalibrationRecord(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_number = models.CharField(max_length=10, 
                                    validators = [RegexValidator(r'^[A-Z]{2}[0-9]{8}$', 'Ten characters starting with two alphabets and ending with eight numbers are allowed.')],
                                    help_text = "Enter a job number, e.g., JN20222511",
                                    verbose_name = 'Job Number')
    site_id = models.ForeignKey(CalibrationSite,
                                    limit_choices_to=Q(site_type = 'staff_range') | Q(site_type = 'staff_lab'),  
                                    null = True,
                                    on_delete = models.RESTRICT, 
                                    verbose_name = 'Site Name')
    inst_staff = models.ForeignKey(Staff, 
                                    null=True,
                                    on_delete = models.RESTRICT, 
                                    verbose_name = 'Staff Number')
    inst_level = models.ForeignKey(DigitalLevel, 
                                    null=True,
                                    on_delete = models.RESTRICT, 
                                    verbose_name = 'Level Number')
    ave_temperature1 = models.FloatField(help_text = "Average temperature for the first set")
    ave_temperature2 = models.FloatField(help_text = "Average temperature for the second set")
    calibration_date = models.DateField()
    
    calibration_report = models.FileField(upload_to = get_upload_to_calibreport,
                                        null=True,
                                        blank=True,
                                        verbose_name= 'Calibration Certificate/Report')
    field_file = models.FileField(upload_to = get_upload_to_fieldfile,
                                        null=True,
                                        help_text = 'Upload the ASCII file generated by the level instrument',
                                        verbose_name= 'Field Data')
    field_book = models.FileField(upload_to = get_upload_to_fieldbook,
                                        null=True,
                                        help_text = 'Upload the field book in pdf/jpg/tif format',
                                        verbose_name= 'Field Book')
    observer_isme = models.BooleanField(default=False, verbose_name = "I am the Observer")
    observer = models.CharField(max_length=50, null=True, blank=True)
    valid = models.BooleanField(default=True, verbose_name = "Calibration Valid")
    updated_to = models.BooleanField(default=False, verbose_name = "Updated to Range Param")
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['site_id', 'job_number', 'inst_staff', 'calibration_date'], name = 'unique_calibration_instance'
            ),
        ]
        ordering = ['inst_staff', 'calibration_date']
        # unique_together = ['site_id', 'job_number', 'inst_staff', 'calibration_date']

    def __str__(self):
        return f'{self.job_number} ({self.calibration_date.strftime("%Y-%m-%d")})'

    def staff_type(self):
        return self.inst_staff.staff_type
    def staff_length(self):
        return self.inst_staff.staff_length

    @property
    def report_url(self):
        """
        Return url if self.calibration_report is not None, 
        'url' exist and has a value, else, return None.
        """
        if self.calibration_report:
            return getattr(self.calibration_report, 'url', None)
        return None
    
    @property
    def fieldbook_url(self):
        """
        Return url if self.field_book is not None, 
        'url' exist and has a value, else, return None.
        """
        if self.field_book:
            return getattr(self.field_book, 'url', None)
        return None
    
    @property
    def fieldfile_url(self):
        """
        Return url if self.field_file is not None, 
        'url' exist and has a value, else, return None.
        """
        if self.field_file:
            return getattr(self.field_file, 'url', None)
        return None

# Raw data model
class RawDataModel(models.Model):
    calibration_id = models.ForeignKey(RangeCalibrationRecord, 
                            null = True,
                            on_delete = models.RESTRICT,
                            verbose_name = 'Calibration Id')
    observation = models.JSONField(null=True)
  
    def __str__(self):
        return f'{self.calibration_id.job_number}-{self.calibration_id.inst_staff.staff_number} ({self.calibration_id.calibration_date.strftime("%Y-%m-%d")})'

    def job_number(self):
        return self.calibration_id.job_number

    def staff_number(self):
        return self.calibration_id.inst_staff.staff_number
    
    def staff_type(self):
        return self.calibration_id.inst_staff.staff_type
    
    def staff_length(self):
        return self.calibration_id.inst_staff.staff_length

    def level_number(self):
        return self.calibration_id.inst_level.level_number

    def calibration_date(self):
        return self.calibration_id.calibration_date

# Adjustment data model
class AdjustedDataModel(models.Model):
    calibration_id = models.ForeignKey(RangeCalibrationRecord, 
                            null = True,
                            on_delete = models.RESTRICT,
                            verbose_name = 'Calibration Id')
    adustment = models.JSONField(null=True)
  
    def __str__(self):
        return f'{self.calibration_id.job_number} ({self.calibration_id.calibration_date.strftime("%Y-%m-%d")})'
    
    def job_number(self):
        return self.calibration_id.job_number

    def staff_number(self):
        return self.calibration_id.inst_staff.staff_number
    
    def staff_type(self):
        return self.calibration_id.inst_staff.staff_type
    
    def staff_length(self):
        return self.calibration_id.inst_staff.staff_length

    def level_number(self):
        return self.calibration_id.inst_level.level_number

    def calibration_date(self):
        return self.calibration_id.calibration_date

# Adjusted height difference data model
class HeightDifferenceModel(models.Model):
    calibration_id = models.ForeignKey(RangeCalibrationRecord, 
                            null = True,
                            on_delete = models.RESTRICT,
                            verbose_name = 'Calibration Id')
    height_difference = models.JSONField(null=True)
  
    def __str__(self):
        return f'{self.calibration_id.job_number} ({self.calibration_id.calibration_date.strftime("%Y-%m-%d")})'

    def job_number(self):
        return self.calibration_id.job_number

    def staff_number(self):
        return self.calibration_id.inst_staff.staff_number
    
    def staff_type(self):
        return self.calibration_id.inst_staff.staff_type
    
    def staff_length(self):
        return self.calibration_id.inst_staff.staff_length

    def level_number(self):
        return self.calibration_id.inst_level.level_number

    def calibration_date(self):
        return self.calibration_id.calibration_date
    
# Boya Range Parameters
def get_month_list():
    return {
        '1': 'Jan', 
        '2': 'Feb',
        '3': 'Mar',
        '4': 'Apr',
        '5': 'May',
        '6': 'Jun',
        '7': 'Jul',
        '8': 'Aug',
        '9': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec',
    }
class BarCodeRangeParam(models.Model):
    site_id = models.ForeignKey(CalibrationSite, 
                                null = True,
                                on_delete = models.RESTRICT,
                                verbose_name = 'Calibration Site')
    
    from_to = models.JSONField(null=True, blank=True)
    Jan = models.JSONField(null=True, blank=True)
    Feb = models.JSONField(null=True, blank=True)
    Mar = models.JSONField(null=True, blank=True)
    Apr = models.JSONField(null=True, blank=True)
    May = models.JSONField(null=True, blank=True)
    Jun = models.JSONField(null=True, blank=True)
    Jul = models.JSONField(null=True, blank=True)
    Aug = models.JSONField(null=True, blank=True)
    Sep = models.JSONField(null=True, blank=True)
    Oct = models.JSONField(null=True, blank=True)
    Nov = models.JSONField(null=True, blank=True)
    Dec = models.JSONField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    modified_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.site_id} - Pin --> {self.from_to}'
# class RangeParameters(models.Model):
#     pin = models.CharField(max_length=10, primary_key=True)
#     Jan = models.FloatField(null=True)
#     Feb = models.FloatField(null=True)
#     Mar = models.FloatField(null=True)
#     Apr = models.FloatField(null=True)
#     May = models.FloatField(null=True)
#     Jun = models.FloatField(null=True)
#     Jul = models.FloatField(null=True)
#     Aug = models.FloatField(null=True)
#     Sep = models.FloatField(null=True)
#     Oct = models.FloatField(null=True)
#     Nov = models.FloatField(null=True)
#     Dec = models.FloatField(null=True)
    
#     def __str__(self):
#         return self.pin