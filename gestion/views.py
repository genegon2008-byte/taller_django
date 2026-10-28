# LIBRERIAS
import json

from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Proyecto


# VISTA
@method_decorator(csrf_exempt, name="dispatch")
class ProyectoView(View):

    # GET -> READ (listar todos o consultar uno)
    def get(self, request, pk=None):
        if pk:
            proyecto = get_object_or_404(Proyecto, pk=pk)
            return JsonResponse(model_to_dict(proyecto))
        proyectos = list(Proyecto.objects.values())
        return JsonResponse(proyectos, safe=False)

    # POST -> CREATE (crear un registro)
    def post(self, request):
        try:
            datos = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        proyecto = Proyecto.objects.create(**datos)
        return JsonResponse(model_to_dict(proyecto), status=201)

    # PUT -> UPDATE (actualizar un registro)
    def put(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        try:
            datos = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        for campo, valor in datos.items():
            setattr(proyecto, campo, valor)
        proyecto.save()
        return JsonResponse(model_to_dict(proyecto))

    # DELETE -> DELETE (eliminar un registro)
    def delete(self, request, pk):
        proyecto = get_object_or_404(Proyecto, pk=pk)
        proyecto.delete()
        return JsonResponse({"mensaje": "Proyecto eliminado"})
