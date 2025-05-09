from django.http import HttpResponseNotFound
from django.template import Context
from django.template.loader import get_template

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Si el error es 404, lo manejamos aquí
        if response.status_code == 404:
            try:
                # Cargar una plantilla 404 directamente en el middleware sin necesidad de DEBUG
                template = get_template('404.html')
                content = template.render(Context())
                return HttpResponseNotFound(content)
            except Exception as e:
                # Si no encuentra la plantilla, manejar el error como una respuesta genérica
                return HttpResponseNotFound('<h1>Página no encontrada</h1>')
        
        return response
