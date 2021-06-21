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
from pcs.models import *

from organisation_structure.models import *


logger = logging.getLogger('django.template')
BASE_DIR = Path(__file__).resolve().parent.parent


def activities(request):
    context = {}
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=12)

    user_current_proj_id = user_project_mapping.objects.get(user=request.user.id)
    user_current_proj_name = project_info.objects.get(id=user_current_proj_id.id)
    context['cp'] = user_current_proj_name
    context['current_pid'] = user_current_proj_id.id

    f = open(os.path.join(BASE_DIR, 'debug4.log'), 'r')
    now = datetime.datetime.now()
    pdf.cell(20, 4, txt="Prudent Aire                                                                "
                        "                                                         "
                        " VAV Selection", ln=1, align='L',)
    #pdf.cell(40, 2, txt="Date Generated: " + now.strftime("%Y-%m-%d %H:%M:%S"), ln=1, align='R')
    pdf.cell(40, 2, txt="", ln=1, align='R')
    context['cart'] = cart.objects.filter(user=request.user.id)
    cart_items = cart.objects.filter(user=request.user.id)

    for c in cart_items:
        pdf.cell(200, 10, txt=str(c.size) + " -- " + str(c.design_airflow), ln=1, align='L')
    f.close()
    pdf.output(os.path.join(BASE_DIR, 'activities_report.pdf'))
    with open(os.path.join(BASE_DIR, 'debug4.log'), 'r') as f:
        flist = []

        for x in reversed(f.readlines()):
            flist.append(x.rstrip())


    return render(request, 'activities.html', context)

def download_file(request):
    fl_path = os.path.join(BASE_DIR, 'activities_report.pdf')
    filename = 'activities_report.pdf'
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response



class GRD(LoginRequiredMixin, TemplateView):
    template_name = 'grd.html'
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
        user_current_proj_id = user_project_mapping.objects.get(user=self.request.user.id)
        user_current_proj_name = project_info.objects.get(id=user_current_proj_id.id)
        kwargs['current_project'] = user_current_proj_name.project_name
        kwargs['current_pid'] = user_current_proj_id.id
        kwargs['cart'] = cart.objects.filter(user=self.request.user.id)
        return super(VAV, self).get_context_data(**kwargs)

vav_input_data = {}

def test(request):
    vav_input_data.clear()
    context = {}
    tag = request.POST.get('tag', False)
    quantity = request.POST.get('quantity', False)
    if not quantity:
        quantity = 1
    ahu = request.POST.get('ahu', False)
    airflow_input = request.POST.get('airflow', False)
    min_cfm = request.POST.get('min_airflow',False)

    user_current_proj_id = user_project_mapping.objects.get(user=request.user.id)
    user_current_proj_name = project_info.objects.get(id=user_current_proj_id.id)
    context['current_project'] = user_current_proj_name.project_name
    context['current_pid'] = user_current_proj_id.id

    if not min_cfm:
        min_cfm = int(float(airflow_input)*0.3)

    #print(vav_input_data)
    pid = request.POST.get('pid')
    size = request.POST.get('size')
    attenuator = request.POST.get('attenuator')
    outlet_type = request.POST.get('outlet_type')
    insulation = request.POST.get('insulation')
    controls = request.POST.get('controls')
    vav_input_data['size'] = size
    vav_input_data['design_airflow'] = airflow_input
    vav_input_data['minimum_cfm'] = min_cfm
    vav_input_data['attenuator'] = attenuator
    vav_input_data['outlet_type'] = outlet_type
    vav_input_data['insulation'] = insulation
    vav_input_data['controls'] = controls
    vav_input_data['pid'] = pid
    vav_input_data['tag'] = tag
    vav_input_data['quantity'] = quantity
    vav_input_data['ahu'] = ahu

    select_cfm_query = airflow.objects.filter(cfm_max__gte=airflow_input)[:3]
    display_queryset = performance.objects.none()
    radiated_queryset = radiated_acoustic_data.objects.none()
    discharge_queryset = discharge_acoustic_data.objects.none()
    for rows in select_cfm_query:
        performance_query = performance.objects.filter(size_inch=rows.size_inch).extra(
            select={"cfm_new": "abs(cfm-"+airflow_input+")"}).order_by("cfm_new")[:1]
        display_queryset |= performance_query

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
    context['airflow_input'] = airflow_input
    context['min_airflow'] = min_cfm
    context['tag'] = tag
    context['quantity'] = quantity
    context['ahu'] = ahu

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
    return redirect('/vav/')

class CommonView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = "projectInfo.html"

    def get_context_data(self, **kwargs):
        kwargs['cart'] = cart.objects.filter(user=self.request.user.id)
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
        date_string = ""
        p_name = self.request.GET.get("p_name", None)
        p_info = project_info.objects.filter(project_name=p_name)
        for dt in p_info:
            date_string = str(dt.project_date)
            pid = dt.id
        user_current_proj_id = user_project_mapping.objects.get(user=self.request.user.id)
        user_current_proj_name = project_info.objects.get(id=user_current_proj_id.id)
        print(user_current_proj_id.id, user_current_proj_name.project_name)

        if p_name:
            user_project_update = user_project_mapping.objects.get(user=self.request.user.id)
            user_project_update.project = pid
            user_project_update.save()

        kwargs['ps'] = p_info
        kwargs['pd'] = date_string
        kwargs['name5'] = 'active'
        kwargs['cart'] = cart.objects.filter(user=self.request.user.id)
        kwargs['projects'] = project_info.objects.filter(user=self.request.user.id)
        kwargs['current_project'] = user_current_proj_name.project_name
        kwargs['current_pid'] = user_current_proj_id.id

        return super(ProjectView, self).get_context_data(**kwargs)


class loginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        return super(loginView, self).get_context_data(**kwargs)

def maintenance(request):
    return render(request,'maintenance.html')

def construction(request):
    return render(request,'siteunderconstruction.html')


