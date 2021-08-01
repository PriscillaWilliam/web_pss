import json

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView
import logging
from django.contrib import messages
from django.utils import timezone
import datetime
from fpdf import FPDF
from django.urls import reverse_lazy
import mimetypes
from django.http import JsonResponse
from django.core import serializers
import math
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from pathlib import Path
from django.shortcuts import render
from pss.models import *
import django.contrib.auth

from organisation_structure.models import *


logger = logging.getLogger('django.template')
BASE_DIR = Path(__file__).resolve().parent.parent


def activities(request):
    print("Summary", request.user, datetime.datetime.now())
    now = datetime.datetime.now()
    context = {}
    pdf = FPDF()
    user_current_proj_checker = user_project_mapping.objects.filter(user=request.user.id)
    if user_current_proj_checker:
        user_current_proj_id = user_project_mapping.objects.get(user=request.user.id)
        user_current_proj_name = project_info.objects.get(id=user_current_proj_id.project)
        context['cp'] = user_current_proj_name
        context['current_pid'] = user_current_proj_id.project
        context['cart'] = cart.objects.filter(user=request.user.id, project=user_current_proj_id.project)
        cart_items = cart.objects.filter(user=request.user.id, project=user_current_proj_id.project)
        tag_name_none = False
        if cart_items:
            for c in cart_items:
                if c.tag:
                    tag_name_none = True

        if cart_items:
            i = 1
            for c in cart_items:
                '''pdf.cell(20, 10, txt=str(c.vav_size), align="R")
                pdf.cell(10)
                pdf.cell(20, 10, txt=str(c.design_airflow), align="R")
                pdf.cell(20, 10, txt=str(c.min_airflow), align="R", ln=1)
                '''
                pdf.add_page()
                pdf.set_font("Times", size=12,style='B')
                pdf.set_left_margin(15)
                pdf.set_right_margin(15)
                pdf.image(os.path.join(BASE_DIR, "static\\assets\\img\\pa_logo.png"), 12, 10, 50, 10)
                pdf.line(15, 20, 195, 20)
                pdf.line(15, 45, 195, 45)

                #pdf.cell(25, 4, txt="PRUDENT AIRE", align='L')
                pdf.cell(145)
                pdf.set_font("Times", size=14, style='B')

                pdf.cell(20, 10, txt="VAV Selection", ln=1, align='L', )
                pdf.set_font("Times", size=12, style='B')
                pdf.cell(20, 6, txt="", ln=1, align='L')

                pdf.rect(15, 21, 180, 10)
                #pdf.rect(15.5, 22.5, 179, 9)
                pdf.rect(130, 90, 65, 30)
                pdf.rect(15, 90, 65, 30)

                # pdf.cell(40, 2, txt="Date: " + now.strftime("%Y-%m-%d %H:%M:%S"), ln=5, align='R')
                pdf.cell(20, 1, txt="Project Name:  " + user_current_proj_name.project_name, align='L')
                pdf.cell(110)
                #pdf.cell(20, 2, txt="Tag:  " + str(user_current_proj_name.project_date), ln=1, align='L')
                given_tag = ""
                if not tag_name_none:
                    given_tag = "VAV-"+str(i).zfill(2)
                if c.tag:
                    given_tag = c.tag

                pdf.cell(20, 1, txt="Tag:  " + given_tag, ln=1, align='L')
                #print(str(i).zfill(2))
                pdf.ln(8)
                pdf.set_font("Times", size=12,style='')
                pdf.cell(20, 2, txt="Project Number:  " + user_current_proj_name.project_number, align='L')
                pdf.cell(90)
                pdf.cell(35, 2, txt="Project Location:  ", align='L')
                pdf.cell(20, 2, txt=str(user_current_proj_name.location), ln=1, align='L')
                pdf.ln(3)
                pdf.cell(20, 2, txt="Consultant Name:  " + user_current_proj_name.consultant_name, align='L')
                pdf.cell(90)
                pdf.cell(35, 2, txt="Project Date:  ", align='L')
                pdf.cell(20, 2, txt=user_current_proj_name.project_date.strftime("%d-%m-%Y"), ln=1, align='L')
                pdf.ln(10)
                pdf.ln(2)
                pdf.set_font("Times", size=12,style='B')
                pdf.cell(20,2,txt="Selection ",ln=1)
                pdf.set_font("Times", size=10,style='')
                pdf.ln(2)
                pdf.cell(30, 12, txt="Quantity", border=1, align='C')
                pdf.cell(30, 12, txt="VAV Size", border=1, align='C')
                pdf.cell(60, 6, txt="Units in "+user_current_proj_name.units, border=1, align='C')
                pdf.cell(60, 6, txt="Max NR Levels", border=1, align='C', ln=1)
                pdf.cell(60)
                pdf.cell(30, 6, txt="Design airflow", border=1, align='C')
                pdf.cell(30, 6, txt="Min. airflow", border=1,  align='C')
                pdf.cell(30, 6, txt="Discharge NR", border=1,  align='C')
                pdf.cell(30, 6, txt="Radiated NR", border=1,  align='C', ln=1)
                pdf.cell(30, 6, txt=str(c.quantity), border=1, align='C')
                pdf.cell(30, 6, txt=str(c.vav_size), border=1, align='C')
                pdf.cell(30, 6, txt=str(c.design_airflow), border=1, align='C')
                pdf.cell(30, 6, txt=str(c.min_airflow), border=1, align='C')
                pdf.cell(30, 6, txt=str(c.dNR), border=1, align='C')
                pdf.cell(30, 6, txt=str(c.rNR), border=1, align='C', ln=1)
                pdf.ln(10)
                pdf.set_font("Times", size=12, style='B')
                pdf.cell(20, 2, txt="Other Information ",align='L')
                pdf.cell(95)
                pdf.cell(20, 2, txt="Accessories ",align='L')
                pdf.ln(4)
                pdf.cell(120)
                pdf.set_font("Times", size=10, style='B')
                pdf.cell(20, 3, ln=1,align='R')
                pdf.cell(10)
                pdf.cell(25, 6, txt="Maximum "+user_current_proj_name.units+":  ", align='R')
                airflow_data = airflow.objects.get(size_inch = c.vav_size)
                max_units = airflow_data.cfm_max
                min_units = airflow_data.cfm_min
                units = user_current_proj_name.units
                if units == "CMH":
                    max_units = int(float(max_units) * 1.7)
                    min_units = int(float(min_units) * 1.7)
                elif units == "L/S":
                    max_units = int(float(max_units) / 2.118)
                    min_units = int(float(min_units) / 2.118)
                #print(str(100-int(c.design_airflow/max_units*100))+"%")
                pdf.set_font("Times", size=10, style='')
                pdf.cell(20, 6, txt=str(max_units), align='L')
                pdf.cell(65)
                pdf.set_font("Times", size=10, style='B')
                pdf.cell(20, 6, txt="Outlet:  ", align='R')
                pdf.set_font("Times", size=10, style='')
                pdf.cell(20, 6, txt=str(c.outlet_type), align='L', ln=1)
                pdf.set_font("Times", size=10, style='B')
                pdf.cell(10)
                pdf.cell(25, 6, txt="Minimum " + user_current_proj_name.units + ":  ", align='R')
                pdf.set_font("Times", size=10, style='')
                pdf.cell(20, 6, txt=str(min_units), align='L')
                pdf.cell(65)
                pdf.set_font("Times", size=10, style='B')
                pdf.cell(20, 6, txt="Insulation:  ", align='R')
                pdf.set_font("Times", size=10, style='')
                pdf.cell(20, 6, txt=str(c.insulation), align='L', ln=1)
                pdf.set_font("Times", size=10, style='B')
                pdf.cell(10)
                pdf.cell(25, 6, txt="Design " + user_current_proj_name.units + ":  ", align='R')
                pdf.set_font("Times", size=10, style='')
                pdf.cell(20, 6, txt=str(c.design_airflow), align='L')
                pdf.cell(65)
                pdf.set_font("Times", size=10, style='B')
                pdf.cell(20, 6, txt="Attenuator:  ", align='R')
                pdf.set_font("Times", size=10, style='')
                pdf.cell(20, 6, txt=str(c.attenuator), align='L', ln=1)
                pdf.set_font("Times", size=10, style='B')
                pdf.cell(10)
                pdf.cell(25, 6, txt="Safety Factor :  ", align='R')
                pdf.set_font("Times", size=10, style='')
                pdf.cell(20, 6, txt=str(100 - int(c.design_airflow / max_units * 100)) + "%", align='L')
                pdf.cell(65)
                pdf.set_font("Times", size=10, style='B')
                pdf.cell(20, 6, txt="Controls:  ", align='R')
                pdf.set_font("Times", size=10, style='')
                pdf.cell(20, 6, txt=str(c.controls), align='L', ln=1)
                pdf.ln(15)
                pdf.set_font("Times", size=12, style='B')
                pdf.cell(20, 2, txt="Acoustic Summary ", ln=1)
                pdf.set_font("Times", size=10, style='')
                pdf.ln(2)

                pdf.cell(40, 4, txt="", border=1, align='C')
                pdf.cell(20, 4, txt="125Hz", border=1, align='C')
                pdf.cell(20, 4, txt="250Hz", border=1, align='C')
                pdf.cell(20, 4, txt="500Hz", border=1, align='C')
                pdf.cell(20, 4, txt="1000Hz", border=1, align='C')
                pdf.cell(20, 4, txt="2000Hz", border=1, align='C')
                pdf.cell(20, 4, txt="4000Hz", border=1, align='C')
                pdf.cell(20, 4, txt="NR", border=1, align='C',ln=1)
                pdf.cell(40, 10, txt="Discharge Acoustic Data", border=1, align='C')
                d_acdata = discharge_acoustic_data.objects.filter(size_inch=c.vav_size, cfm=c.cfm)
                for d in d_acdata:
                #r_acdata = radiated_acoustic_data.objects.get(cfm=c.cfm)
                    pdf.cell(20, 10, txt=str(d.Hz125), border=1, align='C')
                    pdf.cell(20, 10, txt=str(d.Hz250), border=1, align='C')
                    pdf.cell(20, 10, txt=str(d.Hz500), border=1, align='C')
                    pdf.cell(20, 10, txt=str(d.Hz1000), border=1, align='C')
                    pdf.cell(20, 10, txt=str(d.Hz2000), border=1, align='C')
                    pdf.cell(20, 10, txt=str(d.Hz4000), border=1, align='C')
                    pdf.cell(20, 10, txt=str(c.dNR), border=1, align='C', ln=1)
                pdf.cell(40, 10, txt="Radiated Acoustic Data", border=1, align='C')
                r_acdata = radiated_acoustic_data.objects.filter(size_inch=c.vav_size, cfm=c.cfm)
                for r in r_acdata:
                    pdf.cell(20, 10, txt=str(r.Hz125), border=1, align='C')
                    pdf.cell(20, 10, txt=str(r.Hz250), border=1, align='C')
                    pdf.cell(20, 10, txt=str(r.Hz500), border=1, align='C')
                    pdf.cell(20, 10, txt=str(r.Hz1000), border=1, align='C')
                    pdf.cell(20, 10, txt=str(r.Hz2000), border=1, align='C')
                    pdf.cell(20, 10, txt=str(r.Hz4000), border=1, align='C')
                    pdf.cell(20, 10, txt=str(c.rNR), border=1, align='C', ln=1)
                pdf.ln(10)
                pdf.set_font("Times", size=11, style='')
                pdf.cell(20,6, txt="Notes : ", align='L', ln=1)
                pdf.cell(5)
                pdf.cell(20,6, txt="1. Selections are based on Prudent Aire as Manufacturer.", align='L', ln=1)
                pdf.cell(5)
                pdf.cell(20,6, txt="2. All performance based on tests conducted in accordance with ASHRAE 130-2008 and ARI 880-2011.", align='L', ln=1)
                pdf.cell(5)
                pdf.cell(20,6, txt="3. All NR levels determined using ARI 885-2008.", align='L', ln=1)
                pdf.cell(5)
                pdf.cell(20,6, txt="4. All airflow, pressure losses and performance values have been corrected for altitude.", align='L', ln=1)
                pdf.cell(5)
                pdf.cell(20,6, txt="5. Units of measure: airflow (cfm, cmh, l/s), air pressure (in pa)", align='L', ln=1)
                pdf.ln(57)
                pdf.set_font("Times", size=9, style='')
                pdf.cell(180,4,txt="The results of this program are only an aid to the designer, " \
                                   "and are not a substitute for professional design services.",align='C',ln=1)
                pdf.cell(180, 4, txt="All data subject to change without notice.",align='C',ln=1 )
                pdf.ln(4)
                pdf.cell(20, 1, txt="Printed : " + now.strftime("%d.%m.%Y %I:%M%p"),align='L')
                pdf.cell(150)
                pdf.cell(20, 1, txt='Page : '+str(pdf.page_no()), align='L')


                #pdf.ln(6)
                #pdf.cell(20, 2, txt="Printed", align='C', ln=1)


                i+=1

    else:
        context['cp'] = None
        context['current_pid'] = None
        context['cart'] = None



    '''
    pdf.add_page()
    pdf.set_font("Times", size=12)    
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    pdf.line(15, 15, 195, 15)
    pdf.cell(20, 4, txt="Prudent Aire",align='L')
    pdf.cell(125)
    pdf.cell(20, 4, txt="VAV Selection", ln=1, align='L', )
    pdf.cell(20, 6, txt="", ln=1, align='L')

    pdf.rect(15,17,180,9)

    #pdf.cell(40, 2, txt="Date: " + now.strftime("%Y-%m-%d %H:%M:%S"), ln=5, align='R')

    user_current_proj_checker = user_project_mapping.objects.filter(user=request.user.id)

    if user_current_proj_checker:
        user_current_proj_id = user_project_mapping.objects.get(user=request.user.id)
        user_current_proj_name = project_info.objects.get(id=user_current_proj_id.project)
        context['cp'] = user_current_proj_name
        context['current_pid'] = user_current_proj_id.project
        context['cart'] = cart.objects.filter(user=request.user.id, project=user_current_proj_id.project)
        pdf.cell(20, 2, txt="Project Name:  " + user_current_proj_name.project_name, align='L')
        pdf.cell(110)
        pdf.cell(20, 2, txt="Tag:  " + str(user_current_proj_name.project_date), ln=1, align='L')
        pdf.ln(7)
        pdf.set_left_margin(25)
        pdf.cell(20, 2, txt="Project Number: " + user_current_proj_name.project_number , align='L')
        pdf.cell(90)
        pdf.cell(20, 2, txt="Project Location: " + str(user_current_proj_name.location), ln=1, align='L')
        pdf.ln(7)
        
    else:
        context['cp'] = None
        context['current_pid'] = None
        context['cart'] = None
    '''
    pdf.output(os.path.join(BASE_DIR, 'SelectionReport.pdf'))
    return render(request, 'activities.html', context)


def download_file(request):
    fl_path = os.path.join(BASE_DIR, 'SelectionReport.pdf')
    filename = 'SelectionReport.pdf'
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


class GRD(LoginRequiredMixin, TemplateView):
    #template_name = 'grd.html'
    template_name = 'siteunderconstruction.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        return redirect(reverse_lazy('vav'))

    def get_context_data(self, **kwargs):
        kwargs['name'] = 'active'
        return super(GRD, self).get_context_data(**kwargs)

class VAV(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = "vav.html"

    def get_context_data(self, **kwargs):
        user_current_proj_checker = user_project_mapping.objects.filter(user=self.request.user.id)
        if user_current_proj_checker:
            user_current_proj_id = user_project_mapping.objects.get(user=self.request.user.id)
            user_current_proj_name = project_info.objects.get(id=user_current_proj_id.project)
            kwargs['current_project'] = user_current_proj_name.project_name
            kwargs['units'] = user_current_proj_name.units
            kwargs['current_pid'] = user_current_proj_id.project
            kwargs['cart'] = cart.objects.filter(user=self.request.user.id,project=user_current_proj_id.project)
        else:
            kwargs['current_project'] = None
            kwargs['current_pid'] = None
            kwargs['cart'] = None
            kwargs['units'] = "CFM"
        return super(VAV, self).get_context_data(**kwargs)

vav_input_data = {}

def delete(request):
    item = request.POST.get('delete')
    cart_items = cart.objects.get(id=item)
    cart_items.delete()
    return redirect('/vav/')

def test(request):
    vav_input_data.clear()
    context = {}
    tag = request.POST.get('tag', False)
    quantity = request.POST.get('quantity', False)
    units = request.POST.get('units')

    if not quantity:
        quantity = 1
    ahu = request.POST.get('ahu', False)
    airflow_input_ori = request.POST.get('airflow', False)
    min_cfm = request.POST.get('min_airflow',False)

    if units=="CFM":
        airflow_input = airflow_input_ori
    elif units=="CMH":
        airflow_input = int(float(airflow_input_ori)/1.7)
        airflow_input = str(airflow_input)

    elif units=="L/S":
        airflow_input = int(float(airflow_input_ori)*2.118)
        airflow_input = str(airflow_input)


    user_current_proj_checker = user_project_mapping.objects.filter(user=request.user.id)
    if user_current_proj_checker:
        user_current_proj_id = user_project_mapping.objects.get(user=request.user.id)
        user_current_proj_name = project_info.objects.get(id=user_current_proj_id.project)
        context['current_project'] = user_current_proj_name.project_name
        context['current_pid'] = user_current_proj_id.project
        if user_current_proj_id:
            context['cart'] = cart.objects.filter(user=request.user.id, project=user_current_proj_id.project)
        else:
            context['cart'] = None
    else:
        context['current_project'] = None
        context['current_pid'] = None
        context['cart'] = None

    if not min_cfm:
        min_cfm = int(float(airflow_input_ori)*0.3)

    #print(vav_input_data)
    pid = request.POST.get('pid')
    size = request.POST.get('size')
    attenuator = request.POST.get('attenuator')
    outlet_type = request.POST.get('outlet_type')
    insulation = request.POST.get('insulation')
    controls = request.POST.get('controls')
    delta_p = request.POST.get('delta_p')
    vav_input_data['size'] = size
    vav_input_data['design_airflow'] = airflow_input_ori
    vav_input_data['minimum_cfm'] = min_cfm
    vav_input_data['attenuator'] = attenuator
    vav_input_data['outlet_type'] = outlet_type
    vav_input_data['insulation'] = insulation
    vav_input_data['controls'] = controls
    vav_input_data['delta_p'] = delta_p
    vav_input_data['pid'] = context['current_pid']
    vav_input_data['tag'] = tag
    vav_input_data['quantity'] = quantity
    vav_input_data['ahu'] = ahu
    #print(vav_input_data)

    select_cfm_query = airflow.objects.filter(cfm_max__gte=airflow_input)[:3]
    display_queryset = performance.objects.none()
    radiated_queryset = radiated_acoustic_data.objects.none()
    discharge_queryset = discharge_acoustic_data.objects.none()
    for rows in select_cfm_query:
        performance_query = performance.objects.filter(size_inch=rows.size_inch).extra(
            select={"cfm_new": "abs(cfm-"+airflow_input+")"}).order_by("cfm_new")[:1]
        display_queryset |= performance_query
        '''
        performance_query = performance.objects.only('id', 'size_inch', 'cfm', 'discharge_nr'+delta_col,
                                                     'radiated_nr'+delta_col).filter(size_inch=rows.size_inch).extra(
            select={"cfm_new": "abs(cfm-" + airflow_input + ")"}).order_by("cfm_new")[:1]
        display_queryset |= performance_query
        '''
        '''col_name = ('id', 'size_inch', 'cfm', 'discharge_nr'+delta_col, 'radiated_nr'+delta_col)

        test_q = performance.objects.all().values(*col_name)

        test_q1 = performance.objects.filter(size_inch=rows.size_inch).extra(
            select={"cfm_new": "abs(cfm-" + airflow_input + ")"}).values(*col_name).order_by("cfm_new")[:1]
        performance_query = performance.objects.filter(size_inch=rows.size_inch).extra(
            select={"cfm_new": "abs(cfm-" + airflow_input + ")"}).values(*col_name).order_by("cfm_new")[:1]
        display_queryset |= performance_query
        print(test_q1)
        print(performance_query)
        '''
        print(delta_p)
        for r in performance_query:
            print(r.discharge_nr100)
        radiated_acoustic_query = radiated_acoustic_data.objects.filter(size_inch=rows.size_inch).extra(
            select={"cfm_new": "abs(cfm-"+airflow_input+")"}).order_by("cfm_new")[:1]
        radiated_queryset |= radiated_acoustic_query

        discharge_acoustic_query = discharge_acoustic_data.objects.filter(size_inch=rows.size_inch).extra(
            select={"cfm_new": "abs(cfm-" + airflow_input + ")"}).order_by("cfm_new")[:1]
        discharge_queryset |= discharge_acoustic_query

    zipped_list = zip(display_queryset,discharge_queryset,radiated_queryset)

    #context['data'] = display_queryset
    context['data'] = zipped_list
    context['r_data'] = radiated_queryset
    context['d_data'] = discharge_queryset
    context['airflow_input'] = airflow_input_ori
    context['min_airflow'] = min_cfm
    context['tag'] = tag
    context['quantity'] = quantity
    context['ahu'] = ahu
    context['attenuator'] = attenuator
    context['outlet_type'] = outlet_type
    context['insulation'] = insulation
    context['controls'] = controls
    context['delta_p'] = delta_p
    context['units'] = units

    return render(request, 'vav.html',context)

def disp(request):
    selected_vav = request.POST.get('addVav', False)
    selected_vav_info = selected_vav.split('^')
    cart_item = cart(user=request.user.id
                     , tag=vav_input_data['tag']
                     , quantity=vav_input_data['quantity']
                     , ahu=vav_input_data['ahu']
                     , size=vav_input_data['size']
                     , design_airflow=vav_input_data['design_airflow']
                     , min_airflow=vav_input_data['minimum_cfm']
                     , attenuator=vav_input_data['attenuator']
                     , outlet_type=vav_input_data['outlet_type']
                     , insulation=vav_input_data['insulation']
                     , controls=vav_input_data['controls']
                     , vav_size=selected_vav_info[0]
                     , cfm=selected_vav_info[1]
                     , dNR=selected_vav_info[2]
                     , rNR=selected_vav_info[3]
                     , project=vav_input_data['pid']
                     , product=1
                     )
    #uncomment after testing
    cart_item.save()
    vav_input_data.clear()
    #return render(request, 'vav.html')
    print("Cart item", request.user, datetime.datetime.now())

    return redirect('/vav/')

class CommonView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = "projectInfo.html"

    def get_context_data(self, **kwargs):
        user_current_proj_id = user_project_mapping.objects.get(user=self.request.user.id)
        if user_current_proj_id:
            kwargs['cart'] = cart.objects.filter(user=self.request.user.id, project=user_current_proj_id.project)
        else:
            kwargs['cart'] = None
        kwargs['test'] = "test"
        return super(CommonView, self).get_context_data(**kwargs)


def index(request):
    return render(request, 'index.html')


def read(request):
    return render(request, 'viewimage.html', {'name2': 'active'})


def lost_damage(request):

        return render(request, 'reports.html', {'name3': 'active'})


def inventory(request):
    return render(request, 'inventory.html', {'name4': 'active'})


class ProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'projectInfo.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        print("Login",self.request.user, datetime.datetime.now())
        date_string = ""
        p_name = self.request.GET.get("p_name", None)
        #print(p_name)
        p_info = project_info.objects.filter(id=p_name)
        if p_name:
            p_test = project_info.objects.get(id=p_name)
            pid = p_test.id
        else:
            p_test = None
        if p_info:
            for dt in p_info:
                date_string = str(dt.project_date)
            kwargs['ps'] = p_info

        user_current_proj_checker = user_project_mapping.objects.filter(user=self.request.user.id)
        if user_current_proj_checker:
            user_current_proj_id = user_project_mapping.objects.get(user=self.request.user.id)
            user_current_proj_name = project_info.objects.get(id=user_current_proj_id.project)
            kwargs['cart'] = cart.objects.filter(user=self.request.user.id, project=user_current_proj_id.project)
            kwargs['current_project'] = user_current_proj_name.project_name
            kwargs['current_pid'] = user_current_proj_id.project

            if p_name:
                user_project_update = user_project_mapping.objects.get(user=self.request.user.id)
                user_project_update.project = pid
                user_project_update.save()
                kwargs['cart'] = cart.objects.filter(user=self.request.user.id, project=p_name)
        else:
            kwargs['cart'] = None
            kwargs['current_project'] = None
            kwargs['current_pid'] = None

        kwargs['ps'] = None
        kwargs['p'] = p_test
        kwargs['pd'] = date_string
        kwargs['name5'] = 'active'
        kwargs['projects'] = project_info.objects.filter(user=self.request.user.id)

        return super(ProjectView, self).get_context_data(**kwargs)


def save_project(request):
    new_p_name = request.POST.get("new_p_name", None)
    pid = request.POST.get("pid", None)
    p_number = request.POST.get("p_number", None)
    p_date = request.POST.get("p_date", None)
    location = request.POST.get("location", None)
    city = request.POST.get("city", None)
    state = request.POST.get("state", None)
    engineer = request.POST.get("engineer", None)
    client_name = request.POST.get("client_name", None)
    consultant_name = request.POST.get("consultant_name", None)
    prepared_by = request.POST.get("p_by", None)
    remarks = request.POST.get("remarks", None)
    units = request.POST.get("units")
    if not p_date:
        p_date = datetime.date.today()
    if new_p_name:
        new_project = project_info(user=request.user.id
                                   , project_name=new_p_name
                                   , project_number=p_number
                                   , project_date=p_date
                                   , location=location
                                   , city=city
                                   , state=state
                                   , engineer=engineer
                                   , client_name=client_name
                                   , consultant_name=consultant_name
                                   , prepared_by=prepared_by
                                   , remarks=remarks
                                   , units=units
                                   )
        new_project.save()
        #print(new_project.id)
        new_pid = project_info.objects.get(id = new_project.id)
        user_project_checker = user_project_mapping.objects.filter(user=request.user.id)
        if user_project_checker:
            user_project_update = user_project_mapping.objects.get(user=request.user.id)
            user_project_update.project = new_pid.id
            user_project_update.save()
        else:
            user_project_new_entry = user_project_mapping(user = request.user.id
                                                          , project = new_pid.id)
            user_project_new_entry.save()

    elif pid:
        project_info_update = project_info.objects.get(id=pid)
        project_info_update.project_number = p_number
        project_info_update.project_date = p_date
        project_info_update.location = location
        project_info_update.city = city
        project_info_update.state = state
        project_info_update.engineer = engineer
        project_info_update.client_name = client_name
        project_info_update.consultant_name = consultant_name
        project_info_update.prepared_by = prepared_by
        project_info_update.remarks = remarks
        project_info_update.units = units
        project_info_update.save()
    print("Project added", request.user, datetime.datetime.now())
    return redirect('/vav/')


class loginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        return super(loginView, self).get_context_data(**kwargs)

def maintenance(request):
    return render(request,'maintenance.html')

def construction(request):
    return render(request,'siteunderconstruction.html')

def register(request):
    return render(request,'register.html')

def new_user(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name",None)
    email = request.POST.get("email")
    countrycode = request.POST.get("countryCode")
    phone = request.POST.get("phone")
    phone_number = "+"+countrycode+phone
    password = request.POST.get("password")
    existing_user_check = User.objects.filter(username=email)
    if existing_user_check:
        messages.error(request, 'User already exists')
        return redirect(reverse_lazy('register'))
    else:
        user = User.objects.create_user(username=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = phone_number
        user.is_superuser = False
        user.is_staff = False
        user.save()
        return redirect('/register/')


