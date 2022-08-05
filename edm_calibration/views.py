from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.forms.models import model_to_dict
from django.db.models import Avg

from datetime import datetime
from math import pi, sin, cos, sqrt
from geodepy.geodesy import grid2geo, rho
from common_func.Convert import *
from common_func.SurveyReductions import *
from .forms import (CalibrateEdmForm,
                    CalibrateEdmForm3,
                    )
from .models import (uPillar_Survey,
                     )
from instruments.models import (EDM_Inst,
                    Prism_Inst,
                    Mets_Inst,
                    EDMI_certificate,
                    Mets_certificate)
from calibrationsites.models import (Pillar,
                                     CalibrationSite)
from baseline_calibration.models import (Uncertainty_Budget,
                    Uncertainty_Budget_Source,
                    Certified_Distance,
                    Std_Deviation_Matrix)
from common_func.LeastSquares import (
                    LSA,
                    ISO_test_a,
                    ISO_test_c)
# Create your views here.
    
@login_required(login_url="/accounts/login")
def edm_calibration_home(request):
    if request.user.is_superuser:
        pillar_surveys = uPillar_Survey.objects.all()
    else:        
        pillar_surveys = uPillar_Survey.objects.select_related('edm').filter(
            edm__edm_specs__edm_owner = request.user.company.id)
        
    context = {
        'pillar_surveys': pillar_surveys}
    
    return render(request, 'edm_calibration/Home.html', context)


def clear_cache(request):
    if 'calibrate_e' in request.session:
        del request.session['calibrate_e']
    
    return HttpResponseRedirect('/edm_calibration/calibrate1')


def calibrate1(request, id):
    if 'calibrate_e' in request.session:
        ini_data = request.session['calibrate_e']
    else:
        ini_data = {'computation_date':date.today().isoformat()}
    
    if request.method == 'POST':
        form = CalibrateEdmForm1(request.POST or None)
        if form.is_valid():
            frm=cache_format(form)
            ini_data.update(frm)
            request.session['calibrate_e'] = ini_data
            return HttpResponseRedirect('/edm_calibration/calibrate2')
    else:
        print('Form not Valid')
        form = CalibrateEdmForm1(initial=ini_data)
    return render(request, 'edm_calibration/calibrate.html', {
                'Header':'Calibrate your Electronic Distance Instrumentation (EDMI)',
                'Page': 'Page 1 of 5',
                'BackBtn': False,
                'form': form})


def calibrate2(request):
    if 'calibrate_e' in request.session:
        ini_data = request.session['calibrate_e']
    else:
        ini_data={}
        
    if request.method == 'POST':
        form = CalibrateEdmForm2(request.POST or None)
        if form.is_valid():
            frm=cache_format(form)
            ini_data.update(frm)
            request.session['calibrate_e'] = ini_data
            return HttpResponseRedirect('/edm_calibration/calibrate3')
    else:
        print('Form not Valid')
        form = CalibrateEdmForm2(initial=ini_data)
    return render(request, 'edm_calibration/calibrate.html', {
                'Header':'Instrumentation',
                'Page': 'Page 2 of 5',
                'BackBtn': 'calibrate1',
                'form': form})


def calibrate3(request):
    if 'calibrate_e' in request.session:
        ini_data = request.session['calibrate_e']
    else:
        ini_data={}
    
    if not 'outlier_criterion' in ini_data.keys():
        ini_data['outlier_criterion']=2.0
    
    if request.method == 'POST':
        form = CalibrateEdmForm3(request.POST or None, request.FILES)
        if form.is_valid():
            calibrate_e = {}
            calib = {}
            baseline={}
            instruments={}
            uc_budget = {}
            frm=form.cleaned_data
            print(frm)
            
            edm_clms=['from_pillar',
        		      'to_pillar',
        		      'inst_ht',
        		      'tgt_ht',
        		      'raw_slope_dist',
        		      'raw_temperature',
        		      'raw_pressure',
        		      'raw_humidity']
            raw_edm_obs = csv2dict(frm['edm_file'],edm_clms)

            frm=cache_format(form)
            ini_data.update(frm)
            request.session['calibrate_e'] = ini_data
            
            #----------------- Query appropriate instruments and calibrations -----------------#
            instruments = Instruments_qry(ini_data)
            calib = Calibrations_qry(ini_data)
            
            #----------------- Query Baseline data -----------------#  
            baseline = baseline_qry(ini_data)
            
            #----------------- Query the default Uncertainty -----------------#
            uc_budget = uncertainty_qry(ini_data)
            uc_budget['sources'] = add_calib_uc(uc_budget['sources'], 
                                                       calib,
                                                       instruments,
                                                       ini_data['survey_date'])

            for o in raw_edm_obs.values():
                #----------------- Instrument Corrections -----------------#
                o['Temp'],c = apply_calib(o['raw_temperature'],
                                            ini_data['thermo_calib_applied'], 
                                            calib['them'])
                o['Pres'],c = apply_calib(o['raw_pressure'],
                                            ini_data['baro_calib_applied'],
                                            calib['baro'])
                o['Humid'],c = apply_calib(o['raw_humidity'],
                                            ini_data['hygro_calib_applied'],
                                            calib['hygro'])
                o = (edm_mets_correction(o, 
                                           instruments['edm'],
                                           ini_data['mets_applied']))
                
                o['slope_dist'] = (float(o['raw_slope_dist'] )
                                             + o['Mets_Correction'])
                o['Bay'] = o['from_pillar'] + ' - ' + o['to_pillar']
            
            edm_observations = group_list(raw_edm_obs.values(),
                                            group_by='Bay',
                                            labels_list=['from_pillar',
                                                         'to_pillar'],
                                            avg_list=['inst_ht',
                                                      'tgt_ht',
                                                      'Temp',
                                                      'Pres',
                                                      'Humid',
                                                      'Mets_Correction',
                                                      'raw_slope_dist',
                                                      'slope_dist',],
                                            std_list=['slope_dist'])
            
            edm_trend = edm_std_function(edm_observations, 
                                         uc_budget['stddev_0_adj'])           #y = Ax + B
                           
            matrix_A = []
            matrix_x = []
            matrix_P = []
            for i, o in enumerate(edm_observations.values()):
                o['id']=str(i+1)
                o = (offset_slope_correction(o,
                                          baseline['certifed_dist'],
                                          baseline['certifed_dist'],
                                          baseline['d_radius']))
                  
                o['Reduced_distance'] = (o['slope_dist'] 
                                        + o['Offset_Correction']
                                        + o['Slope_Correction'])

                #----------------- Calculate Uncertainties -----------------#
                o['uc_sources'] = add_certified_dist_uc(o, 
                                                  uc_budget['sources'],
                                                  baseline['std_dev_matrix'],
                                                  baseline['calibrated_baseline'].degrees_of_freedom)
                
                o['uc_sources'] = add_surveyed_uc(o, edm_trend, 
                                                  uc_budget['sources'],
                                                  baseline['certifed_dist'])
                      
                o['uc_budget'] = refline_std_dev(o, 
                                                baseline['certifed_dist'], 
                                                instruments['edm'])
                  
                o['uc_combined'] = sum_uc_budget(o['uc_budget'])
                
                #----------------- Least Squares -----------------#
                #----------------- 6 Parameter least squares adjustment -----------------#
                d_term = ((2*pi*o['Reduced_distance'])
                          / instruments['edm'].edm_specs.unit_length)
                a_row = [1,
                         o['Reduced_distance'],
                         sin(d_term),
                         cos(d_term),
                         sin(2*d_term),
                         cos(2*d_term)]
                matrix_A.append(a_row)
                  
                frm = baseline['certifed_dist'][o['from_pillar']]['distance']
                to = baseline['certifed_dist'][o['to_pillar']]['distance']
                matrix_x.append(abs(float(to) - float(frm))
                                -o['Reduced_distance'])
                  
                P_row = [0]*len(edm_observations)
                P_row[len(matrix_x)-1] = (1/
                                     o['uc_combined']['std_dev']**2)
                matrix_P.append(P_row)
                  
            matrix_y, vcv_matrix, chi_test, residuals = LSA(matrix_A, matrix_x, matrix_P)
            # Check t-student test results to determine if cyclic errors are significant
            if False not in [t['t_test'] for t in matrix_y[2:]]:
                matrix_A=[[a[0], a[1]] for a in matrix_A]
                matrix_y, vcv_matrix, chi_test, residuals = LSA(matrix_A, matrix_x, matrix_P)
            
            for o in edm_observations.values():
                o['residual'] = residuals[o['id']]['residual']
                o['std_residual'] = residuals[o['id']]['std_residual']
            
            ISO_test=[]
            ISO_test.append(ISO_test_a(instruments,
                                       chi_test,
                                       [{'distance':50},
                                        {'distance':100},
                                        {'distance':200},
                                        {'distance':400}, 
                                        {'distance':600}]))
            ISO_test.append(ISO_test_c(matrix_y[0]['value'],
                                       matrix_y[0]['std_dev'],
                                       chi_test))

            #Prepare the context for the template
            edm_observations = list(edm_observations.values())
            context = {'frm':ini_data,
                       'instruments':instruments,
                       'calib':calib,
                       # 'residual_chart':residual_chart,
                       'baseline': baseline,
                       'ISO_test':ISO_test,
                       'edm_observations': edm_observations,
                       # 'Check_Errors':Check_Errors
                       }
            
            return render(request, 'baseline_calibration/calibrate_report.html', context)
    else:
        print('Form not Valid')
        form = CalibrateEdmForm3(initial=ini_data)
    return render(request, 'edm_calibration/calibrate.html', {'Header':'File Uploads',
  	                                                             'Page': 'Page 3 of 5',
  	                                                             'BackBtn': 'calibrate2',
  	                                                             'form': form})
    
@login_required(login_url="/accounts/login")
def calibrate(request):
    ini_data = {'computation_date':date.today().isoformat()}
    form = CalibrateEdmForm(request.POST or None,
                            user=request.user,
                            initial=ini_data)    
    
    if request.method == 'POST':
        form = CalibrateEdmForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            frm=form.cleaned_data
            calib = {}
            baseline={}
            instruments={}
            uc_budget = {}
            edm_clms=['from_pillar',
        		      'to_pillar',
        		      'inst_ht',
        		      'tgt_ht',
        		      'raw_slope_dist',
        		      'raw_temperature',
        		      'raw_pressure',
        		      'raw_humidity']
            raw_edm_obs = csv2dict(frm['edm_file'],edm_clms)
                    
            #----------------- Query appropriate instruments and calibrations -----------------#
            instruments = Instruments_qry(frm)
            calib = Calibrations_qry(frm)
            
            #----------------- Query Baseline data -----------------#  
            baseline = baseline_qry(frm)
            
            #----------------- Query the default Uncertainty -----------------#
            uc_budget = uncertainty_qry(frm)
            uc_budget['sources'] = add_calib_uc(uc_budget['sources'], 
                                                       calib,
                                                       instruments,
                                                       frm['survey_date'])
            
            Check_Errors = validate_survey(frm=frm, 
                                           baseline=baseline,
                                           instruments=instruments,
                                           calibrations=calib,
                                           raw_edm_obs=raw_edm_obs)
            
            if len(Check_Errors['Errors']) > 0:
               msg="<h4>The following errors have been detected:</h4>"
               msg+="<p>"
               for e in Check_Errors['Errors']:
                  msg+="   "+ e +"<br>"
               msg+="</p>"
               msg+="<h4>The following warnings have been detected:</h4>"
               msg+="<p>"
               for w in Check_Errors['Warnings']:
                  msg+="   "+ w +"<br>"
               msg+="</p>"
               return HttpResponse(msg)
            else:
               form.save()
            return redirect('edm_calibration:view_edm_observations')
        
    headers = {'page0':'Pillar Survey Information',
               'page1': 'Instrumentation',
               'page2': 'Error Budget and File Uploads',}
    return render(request, 'edm_calibration/calibrate.html', {
            'Headers': headers,
            'Cancelurl': 'edm_calibration_home',
            'form': form})


from .forms import StepBySteGuideForm
from .models import StepBySteGuideModel

def guide_form(request):
    form = StepBySteGuideForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect ('accounts:user_account')
    context = {
        'form': form
        }
    return render(request, 'edm_calibration/edmi_step_guide_form.html', context)

def step_by_step_guide(request):
    contents = StepBySteGuideModel.objects.filter(guide_types='edmi')[0]
    
    context = {
        'contents': contents
    }
    return render(request, 'edm_calibration/edmi_step_guide.html', context)

