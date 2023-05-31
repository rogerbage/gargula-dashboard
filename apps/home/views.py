# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import loader
from django.urls import reverse
from reality.biology import biology
from reality.geography import eden
from models.group.group import Group
from settings import *
import pandas as pd
import json 
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from os import listdir
import time



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def call_simulation(request):
    print(request)
    variavel = {
        'valora': 'oi',
        'valorb': 'ola',
    }
    inputName = request.POST['groupName']
    gargalo = Group(name=inputName, home=eden)
    gargalo.generate_gargalo(10)
    eden.pass_day()
    info = gargalo.get_info()
    variavel['info'] = info
    family = gargalo.get_family()
    hv = gargalo.hvs[5]
    info_hv = hv.get_info(show_genes=False, show_action=True, show_visible=False)  
    variavel['info_hv'] = info_hv
    genes = hv.get_genes()
    variavel['genes'] = genes.tolist()
    traits = hv.genes.phenotype.traits
    print('traits:', traits)
    variavel['traits'] = traits
    indicators = hv.history.get_indicators()
    print('indicators: ', indicators)
    variavel['indicators'] = indicators
    y_actions = hv.history.get_counter()
    print('y_actions: ', type(y_actions))
    variavel['y_actions'] = list(y_actions)

    data_gene = gargalo.history.get_genes()
    print('data_gene: ', type(data_gene))
    variavel['data_gene'] = data_gene.tolist()
    
    # group_y_genes, group_y_traits, group_y_actions = gargalo.history.get_indicators()
    # # print('group_y: ', group_y_genes, group_y_traits, group_y_actions)

    # gg_y_genes = []
    # for g in group_y_genes:
    #     gg_y_genes[g] = group_y_genes[g]
        
    # print('gg_y_genes: ', gg_y_genes)
    # variavel['group_y_genes'] = gg_y_genes
    # variavel['group_y_traits'] = list(group_y_traits)
    # variavel['group_y_actions'] = list(group_y_actions)


    variavel['family'] = family
    # variavel['profiles'] = gargalo.get_profiles()
    variavel['group_name'] = gargalo.name

    return JsonResponse(variavel)


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
