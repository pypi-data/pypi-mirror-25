from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import Counter
from django.db.models import F


def index(request):

    pages_reached, created = Counter.objects.get_or_create(name_row = "pages_reached") # x can be any value from one to nine
    pages_reached.total_max_hits = F('total_max_hits') + 1
    pages_reached.save()
    pages = Counter.objects.filter(name_row="pages_reached").values("total_max_hits")

    template = loader.get_template('charisma_django/pages/sample_index.html')
    users = User.objects.count()

    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Dashboard'}
    context['total_members'] = users
    context['pages'] = pages

    return HttpResponse(template.render(context,request))

def ui(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Ui'}
    template = loader.get_template('charisma_django/pages/ui.html')
    return HttpResponse(template.render(context,request))

def form(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Form'}
    template = loader.get_template('charisma_django/pages/form.html')
    return HttpResponse(template.render(context, request))

def chart(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Chart'}
    template = loader.get_template('charisma_django/pages/chart.html')
    return HttpResponse(template.render(context, request))

def typography(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'typography'}
    template = loader.get_template('charisma_django/pages/typography.html')
    return HttpResponse(template.render(context, request))

def gallery(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'gallery'}
    template = loader.get_template('charisma_django/pages/gallery.html')
    return HttpResponse(template.render(context, request))

def tables(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Tables'}
    template = loader.get_template('charisma_django/pages/tables.html')
    return HttpResponse(template.render(context, request))

def calendar(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Calendar'}
    template = loader.get_template('charisma_django/pages/calendar.html')
    return HttpResponse(template.render(context, request))

def grid(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Grid'}
    template = loader.get_template('charisma_django/pages/grid.html')
    return HttpResponse(template.render(context, request))

def tour(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Tour'}
    template = loader.get_template('charisma_django/pages/tour.html')
    return HttpResponse(template.render(context, request))

def icons(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Icons'}
    template = loader.get_template('charisma_django/pages/icons.html')
    return HttpResponse(template.render(context, request))

def error(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Error'}
    template = loader.get_template('charisma_django/pages/error.html')
    return HttpResponse(template.render(context, request))

def login(request):
    context = {'breadcrum_parent': 'Home', 'breadcrum_child': 'Login'}
    template = loader.get_template('charisma_django/pages/login.html')
    return HttpResponse(template.render(context, request))