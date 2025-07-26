import requests
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import redirect



def get_tmdb_recommendations(slug):
    API_KEY = settings.TMDB_API_KEY
    urls = {
        "films": f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1",
        "series": f"https://api.themoviedb.org/3/tv/top_rated?api_key={API_KEY}&language=en-US&page=1",
        "anime": f"https://api.themoviedb.org/3/tv/top_rated?api_key={API_KEY}&language=en-US&page=1",
        "toons": f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1",
        "games": "",
        "books": "",
    }

    url = urls.get(slug)
    if not url:
        return []

    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    movie_list = data.get("results", [])[:20]

    # Format for tv/anime
    if slug in ["series", "anime"]:
        for item in movie_list:
            item["title"] = item.get("name")
            item["release_date"] = item.get("first_air_date")

    return movie_list


def home(request, slug="films"):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        if "media_type" in request.POST:
            slug = request.POST.get("media_type")
            return redirect('home', slug=slug)
    
    movie_list = get_tmdb_recommendations(slug)
    
    # PAGINATOR: Show 20 movies per page
    paginator = Paginator(movie_list, 12)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "home/index.html", 
                  {'page_obj': page_obj,
                    'slug': slug,
                     
    })

