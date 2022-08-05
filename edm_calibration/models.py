from django.db import models
from django.core.validators  import MaxValueValidator, MinValueValidator, DecimalValidator
from django.conf import settings
from baseline_calibration.models import (Uncertainty_Budget,
                                    Pillar_Survey)
from instruments.models import EDM_Inst, Prism_Inst, Mets_Inst
from calibrationsites.models import (CalibrationSite, 
                            Pillar)
# Create your models here.
class uPillar_Survey(models.Model):
   calibrated_baseline = models.ForeignKey(Pillar_Survey, on_delete = models.PROTECT, null = False,
             help_text="Baseline certified distances")
   survey_date = models.DateField(null=False, blank=False)
   computation_date = models.DateField(null=False, blank=False)
   observer = models.CharField(max_length=25,
             null = True,
             blank = True,
             )
   weather_type = (
             ('Sunny/Clear','Sunny/Clear'),
             ('Partially cloudy','Partially cloudy'),
             ('Cloudy', 'Cloudy'),
             ('Overcast', 'Overcast'),
             ('Drizzle','Drizzle'),
             ('Raining','Raining'),
             ('Stormy','Stormy'),
             )
   weather = models.CharField(max_length=25,
             choices=weather_type,
             help_text="Weather conditions",
             unique=False,
             )
   job_number = models.CharField(max_length=25,
             help_text="Job reference eg., JN 20212216",
             unique=False,
             )

   edm = models.ForeignKey(EDM_Inst, on_delete = models.PROTECT, null = False,
             help_text="EDM used for survey")
   prism = models.ForeignKey(Prism_Inst, on_delete = models.PROTECT, null = False,
             help_text="Prism used for survey")
   mets_applied = models.BooleanField(default=True,
             verbose_name= 'Atmospheric corrections applied to EDM data',
             help_text="Meterological corrections have been applied in the EDM instrument.")

   thermometer = models.ForeignKey(Mets_Inst, on_delete = models.PROTECT, null = False,
             limit_choices_to={'mets_specs__mets_model__inst_type': 'thermo'},
             help_text="Thermometer used for survey",
             related_name="ufield_thermometer")
   barometer = models.ForeignKey(Mets_Inst, on_delete = models.PROTECT, null = False,
            limit_choices_to={'mets_specs__mets_model__inst_type': 'baro'},
            help_text="Barometer used for survey",
            related_name="ufield_barometer")
   hygrometer = models.ForeignKey(Mets_Inst, on_delete = models.PROTECT, blank=True, null = True,
            limit_choices_to={'mets_specs__mets_model__inst_type': 'hygro'},
            help_text="Hygrometer, if used for survey",
            related_name="ufield_hygrometer")
   thermo_calib_applied = models.BooleanField(default=True,
             verbose_name= 'thermometer calibration corrections applied',
             help_text="The thermometer calibration correction"
              " has been applied prior to data import.")
   baro_calib_applied = models.BooleanField(default=True,
             verbose_name= 'barometer calibration corrections applied',
             help_text="The barometer calibration correction has been applied prior to data import.")
   hygro_calib_applied = models.BooleanField(default=True,
             verbose_name= 'Hygrometer calibration corrections applied',
             help_text="The hygrometer correction has been applied prior to data import.")

   uncertainty_budget = models.ForeignKey(Uncertainty_Budget, on_delete = models.PROTECT, null = False,
             help_text="Preset uncertainty budget")
   outlier_criterion = models.DecimalField(max_digits=2, decimal_places=1, default=2,
             validators=[MinValueValidator(0), MaxValueValidator(5)],
             help_text="Number of standard deviations for outlier detection threashold.")
   fieldnotes_upload = models.FileField(upload_to='fieldnotes/',
             null=True,
             blank=True, 
             verbose_name= 'Scanned fieldnotes')
   uploaded_on = models.DateTimeField(auto_now_add=True, null=True)
   modified_on = models.DateTimeField(auto_now=True, null=True)

   class Meta:
      ordering = ['edm','survey_date']

   def __str__(self):
      return f'{self.job_number} - {self.edm} ({self.survey_date})'


class uEDM_Observation(models.Model):
   pillar_survey = models.ForeignKey(uPillar_Survey, on_delete = models.CASCADE, null = False)
   
   from_pillar = models.ForeignKey(Pillar, on_delete = models.CASCADE, null = False)
   to_pillar = models.ForeignKey(Pillar, on_delete = models.CASCADE, null = False,
             related_name='+')
   
   inst_ht = models.DecimalField(
             max_digits=4, decimal_places=3,
             verbose_name= 'Instrument height')
   tgt_ht = models.DecimalField(
             max_digits=4, decimal_places=3,
             verbose_name= 'Target height')

   slope_dist = models.DecimalField(
             max_digits=9, decimal_places=5,
             validators=[MinValueValidator(1), MaxValueValidator(1000)],
             verbose_name= 'slope distance')
   
   temperature = models.FloatField(
             validators = [MinValueValidator(0), MaxValueValidator(50.0)],
             null = True, blank = True)
   pressure = models.FloatField(
             validators = [MinValueValidator(0), MaxValueValidator(1500.0)],
             null = True, blank = True)
   humidity = models.FloatField(
             validators = [MinValueValidator(0), MaxValueValidator(100.0)],
             null = True, blank = True)

   class Meta:
      ordering = ['pillar_survey','from_pillar','to_pillar']
             
   def get_absolute_url(self):
      return reverse('baseline_calibration:EDM_Observation-detail', args=[str(self.id)])

   def __str__(self):
      return f'({self.pillar_survey}): {self.from_pillar} → {self.to_pillar})'


from accounts.models import CustomUser
guideline_types = (
         (None, '--- Select Type ---'),
         ('edmi','EDM Instruments'),
         ('edm', 'EDM Baselines'),
         ('staff','Barcode Staves'), 
         ('range', 'Staff Calibration Range'),
         )

class StepBySteGuideModel(models.Model):
   headline = models.CharField(max_length=200, verbose_name = 'Title')
   guide_types = models.CharField(max_length=20,
                        choices=guideline_types, 
                        null=True,
                        verbose_name = 'Type',
                     )
   content = models.TextField()
   img = models.ImageField('Article Image', blank=True, null=True)
   author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   pub_date = models.DateTimeField(auto_now_add=True, null=True)
   mod_date = models.DateTimeField(auto_now=True, null=True)

   def __str__(self):
      return self.headline
   