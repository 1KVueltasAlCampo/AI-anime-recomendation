from django.http import HttpResponse

def home(request):
    return HttpResponse("Hola mundo, te odio con toda mi existencia")