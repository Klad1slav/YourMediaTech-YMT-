import requests
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator


# Create your views here.

def home(request):
    API_KEY = settings.TMDB_API_KEY
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movie_list = data.get('results', []) [:20] # Get 20 movies(max)
    else:
        movie_list = []

    # PAGINATOR: Show 20 movies per page
    paginator = Paginator(movie_list, 12)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "home/index.html", 
                  {'page_obj': page_obj
    })

