import requests
from django.shortcuts import render
from django.conf import settings


# Create your views here.

def home(request):
    API_KEY = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies = data.get('results', []) [:30]
    else:
        movies = []

    return render(request, "home/index.html", 
                  {'movies': movies
    })

