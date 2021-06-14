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
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    f = open(os.path.join(BASE_DIR, 'debug4.log'), 'r')
    now = datetime.datetime.now()
    pdf.cell(200, 10, txt="Card Management Report", ln=1, align='L')
    pdf.cell(200, 10, txt="Date Generated: " + now.strftime("%Y-%m-%d %H:%M:%S"), ln=1, align='L')
    for x in f:

        if "Reported" in x:
            pdf.cell(200, 10, txt=x[0:19] + " -- " + x[23:], ln=1, align='L')
        elif "successfully" in x:
            pdf.cell(200, 10, txt=x[0:19] + " -- " + x[23:], ln=1, align='L')
        elif "Personalisation failed" in x:
            pdf.cell(200, 10, txt=x[0:19] + " -- " + x[23:], ln=1, align='L')
        else:
            continue
    f.close()
    pdf.output(os.path.join(BASE_DIR, 'activities_report.pdf'))
    with open(os.path.join(BASE_DIR, 'debug4.log'), 'r') as f:
        flist = []

        for x in reversed(f.readlines()):
            flist.append(x.rstrip())
        context = {
            'f_contents': flist
        }

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
        return super(VAV, self).get_context_data(**kwargs)

vav_input_data = {}

def test(request):

    context = {}
    airflow_input = request.POST.get('airflow', False)
    min_cfm = request.POST.get('min_airflow',False)
    if not min_cfm:
        min_cfm = int(float(airflow_input)*0.3)

    print(vav_input_data)
    size = request.POST.get('size')
    attenuator = request.POST.get('attenuator')
    outlet_type = request.POST.get('outlet_type')
    insulation = request.POST.get('insulation')
    controls = request.POST.get('controls')
    vav_input_data['size'] = size;
    vav_input_data['design_airflow'] = airflow_input;
    vav_input_data['minimum_cfm'] = min_cfm;
    vav_input_data['attenuator'] = attenuator;
    vav_input_data['outlet_type'] = outlet_type;
    vav_input_data['insulation'] = insulation;
    vav_input_data['controls'] = controls;

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

    return render(request, 'vav.html',context)

def disp(request):
    selected_vav = request.POST.get('addVav', False)
    min_af = request.POST.get('min_airflow', False)
    print(selected_vav,vav_input_data)
    vav_input_data.clear()
    return render(request, 'vav.html')

class CommonView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = "vav.html"

    def get_context_data(self, **kwargs):
        user_cart = cart.objects.get(user_id=self.request.user.id)
        kwargs['cart'] = cart.objects.filter(user_id=self.request.user.id)
        kwargs['test'] = "test"
        print(user_cart.quantity)
        return super(CommonView, self).get_context_data(**kwargs)


def index(request):
    return render(request, 'index.html')


def read(request):
    return render(request, 'viewimage.html', {'name2': 'active'})


def lost_damage(request):

        return render(request, 'reports.html', {'name3': 'active'})


def inventory(request):
    return render(request, 'inventory.html', {'name4': 'active'})


class settingView(LoginRequiredMixin, TemplateView):
    template_name = 'setting.html'
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, **kwargs):
        kwargs['name5'] = 'active'
        return super(settingView, self).get_context_data(**kwargs)


class loginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        return super(loginView, self).get_context_data(**kwargs)

def maintenance(request):
    return render(request,'maintenance.html')

def construction(request):
    return render(request,'siteunderconstruction.html')


