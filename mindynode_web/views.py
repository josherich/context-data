from django.shortcuts import render
from django.views.decorators.cache import cache_page

# Create your views here.
@cache_page(60 * 30)
def homepage(request):
    return render(request, 'index.html')
