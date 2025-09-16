import requests
from django.core.cache import cache
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import redirect



def get_tmdb_recommendations(slug):
    API_KEY = settings.TMDB_API_KEY
    RAWG_API_KEY = settings.RAWG_API_KEY
    urls = {
        "films": f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1",
        "series": f"https://api.themoviedb.org/3/tv/top_rated?api_key={API_KEY}&language=en-US&page=1",
        "anime": f"https://api.themoviedb.org/3/tv/top_rated?api_key={API_KEY}&language=en-US&page=1",
        "toons": f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1",
        "games": f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&ordering=-rating&page_size=20",
        "books": "",
    }

    url = urls.get(slug)
    if not url:
        return []

    response = requests.get(url)
    if response.status_code != 200:
        return []
    

    data = response.json()
    items_list = data.get("results", [])[:20]

    
    # For TMDB media types
    if slug in ["films", "toons"]:
        for item in items_list:
            item["title"] = item.get("title")
            item["release_date"] = item.get("release_date")
            item["overview"] = item.get("overview", "")
            poster_path = item.get("poster_path")
            if poster_path:
                item["poster_url"] = f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                item["poster_url"] = ""
    elif slug in ["series", "anime"]:
        for item in items_list:
            item["title"] = item.get("name")
            item["release_date"] = item.get("first_air_date")
            item["overview"] = item.get("overview", "")
            poster_path = item.get("poster_path")
            if poster_path:
                item["poster_url"] = f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                item["poster_url"] = ""
    elif slug == "games":

    # Just return list with basic info (no description yet)
        return [
        {
            "slug": game["slug"],
            "title": game.get("name"),
            "release_date": game.get("released"),
            "poster_url": game.get("background_image", ""),
            "overview": ""  # will be filled later
        }
        for game in items_list
    ]

    else:
        # For other types like books or unknown, return empty list
        return []

    return items_list



def home(request, slug="films"):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == "POST":
        if "media_type" in request.POST:
            slug = request.POST.get("media_type")
            return redirect('home', slug=slug)
    
    items_list = get_tmdb_recommendations(slug)
    
    # PAGINATOR: Show 20 movies per page
    paginator = Paginator(items_list, 12)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if slug == "games":
        enriched_list = []
        for game in page_obj.object_list:
            cache_key = f"game_details_{game['slug']}"
            details = cache.get(cache_key)
            if details is None:
                print(f"RAWG REQUEST → fetching details for {game['slug']}")  # check cache hit
                details_url = f"https://api.rawg.io/api/games/{game['slug']}?key={settings.RAWG_API_KEY}"
                details_response = requests.get(details_url)
                if details_response.status_code == 200:
                    details = details_response.json()
                    cache.set(cache_key, details, 86400)  # cache for 24h
                else:
                    details = {}
                    print(f"CACHE HIT → loaded {game['slug']} from cache")  # check cache hit
            game["overview"] = details.get("description_raw", "")
            enriched_list.append(game)
    else:
        enriched_list = page_obj.object_list



    return render(request, "home/index.html", 
                  {'page_obj': page_obj,
                   'enriched_list': enriched_list,
                    'slug': slug,
                     
    })
