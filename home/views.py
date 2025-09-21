import requests
from django.core.cache import cache
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import redirect
from rating_menu.models import MediaItem


def get_tmdb_recommendations(slug, user=None):
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

    # For games: keep unchanged
    if slug == "games":
        url = urls.get(slug)
        if not url:
            return []
        response = requests.get(url)
        if response.status_code != 200:
            return []
        data = response.json()
        items_list = data.get("results", [])[:20]
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

    # For TMDB media types (films, series, anime, toons)
    # If user is provided, try personalized recommendations
    if user is not None and user.is_authenticated:
        # Get user's MediaItems with rating > 7 for the given media type
        user_items = MediaItem.objects.filter(user=user, type=slug, rating__gt=7)
        recommended_items = []
        seen_ids = set()
        for item in user_items:
            # Determine TMDB media type and id
            tmdb_id = item.tmdb_id
            if not tmdb_id:
                continue
            if slug in ["films", "toons"]:
                rec_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/recommendations?api_key={API_KEY}&language=en-US&page=1"
            elif slug in ["series", "anime"]:
                rec_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}/recommendations?api_key={API_KEY}&language=en-US&page=1"
            else:
                rec_url = None

            if not rec_url:
                continue

            rec_response = requests.get(rec_url)
            if rec_response.status_code != 200:
                continue
            rec_data = rec_response.json()
            rec_results = rec_data.get("results", [])[:20]
            for rec_item in rec_results:
                rec_id = rec_item.get("id")
                if rec_id in seen_ids:
                    continue
                seen_ids.add(rec_id)
                # Normalize fields
                if slug in ["films", "toons"]:
                    title = rec_item.get("title")
                    release_date = rec_item.get("release_date")
                else:
                    title = rec_item.get("name")
                    release_date = rec_item.get("first_air_date")
                overview = rec_item.get("overview", "")
                poster_path = rec_item.get("poster_path")
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
                recommended_items.append({
                    "id": rec_id,
                    "title": title,
                    "release_date": release_date,
                    "overview": overview,
                    "poster_url": poster_url,
                })

        if recommended_items:
            # Return up to 20 personalized recommendations
            return recommended_items[:20]

    # If no personalized recommendations or no user, fallback to top_rated
    url = urls.get(slug)
    if not url:
        return []

    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    items_list = data.get("results", [])[:20]

    # Normalize fields for TMDB media types
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
    
    items_list = get_tmdb_recommendations(slug, user=request.user)
    
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
