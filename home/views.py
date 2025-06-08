from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "home/index.html",{
        'films_range': range(5),
        'rows_range': range(5)
    })