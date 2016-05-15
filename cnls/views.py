#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader
from django.core import serializers
from cnls.geojson_serializer_with_id import GeojsonWithIdSerializer
from django.shortcuts import get_object_or_404 #, render, redirect
from django.db.models import get_model
#from django.forms.models import model_to_dict
import csv

from cnls.forms import CustomAdminForm
from cnls.models import ActionNationale, ActionTananarive, ActionRegionale, ActionLocale, TypeIntervention, Cible

# Create your views here.
def home(request):
#    return redirect('http://cartong.github.io/mada-front/dist/atlas/index.html', permanent=True)
    template = loader.get_template('index.html')
    def to_json(echelle):
        return GeojsonWithIdSerializer().serialize(echelle.objects.filter(validation='valide'), srid='4326', use_natural_foreign_keys=True)
# NB GeojsonWithIdSerializer a été configuré pour ne renvoyer que les champs qui sont utilisés dans le popup - comportement à modifier si besoin dans geojson_serializer_with_id.py
    
    return HttpResponse(template.render(Context({
        'actionsN' : to_json(ActionNationale),
        'actionsT' : to_json(ActionTananarive),
        'actionsR' : to_json(ActionRegionale),
        'actionsL' : to_json(ActionLocale),
        'typesinterventions' : TypeIntervention.objects.all(),
        'cibles' : Cible.objects.all(),        
        })))

#def detail(request, action_echelle, action_id):
def detail(request, classe, id):
    template = loader.get_template('detail.html')
    model = get_model('cnls', classe)
    return HttpResponse(template.render(Context({'action' : get_object_or_404(model.objects.prefetch_related(), pk=id)})))

    
def get_geoactions(request):
    def to_json(echelle):
        return GeojsonWithIdSerializer().serialize(echelle.objects.all(), srid='4326', use_natural_foreign_keys=True)
        #return serializers.serialize('geojson', echelle.objects.all(), srid='4326', use_natural_foreign_keys=True)
    
    data = {
        to_json(ActionNationale),
        to_json(ActionTananarive),
        to_json(ActionRegionale),
        to_json(ActionLocale),
        }
#    data = serializers.serialize('geojson', ActionTananarive.objects.all(), srid='4326', use_natural_foreign_keys=True)
    return HttpResponse(data, content_type='application/json')

#def get_faritra(request):
#    faritra = open(djangoSettings.STATIC_ROOT + 'json/faritra.json', 'r')
#    #faritra = serializers.serialize('json', data)
#    return HttpResponse(faritra)


def export_csv(request, ids=None):  
    params = request.GET.getlist('id', default=None)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="CNLS_selection.csv"'

    writer = csv.writer(response)
#    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Cette fonctionnalité est encore en développement.'])
    for pk in params :
#    aaaahhhhhhhhh il faut encore le nom du modèle :-(
#        action = 
        # vérifier si action publique
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
