from django.shortcuts import render, redirect,  get_object_or_404
from django.db import transaction
from .forms import MediaItemForm 
from .models import MediaItem
from django.conf import settings
import requests
import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse

def search_game_rawg(query):
    RAWG_API_KEY = settings.RAWG_API_KEY
    url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&search={query}"
    
    response = requests.get(url)
    data = response.json()

    
    if response.status_code != 200:
        return []

    data = response.json()
    if data['results']:
        game = data['results'][0]  # First matching game
        return {
            'title': game['name'],
            'description': game.get('description_raw', 'No description'),
            'poster_url': game['background_image'],
            'release_date': game['released'],
            'id': game['id'],
            'genre': [g['name'] for g in game.get('genres', [])]
            }
    return []

def search_media_tmdb(query, media_type)->list:
    MOVIE_API_KEY = settings.TMDB_API_KEY
    urls = {
        "films": f"https://api.themoviedb.org/3/search/movie?api_key={MOVIE_API_KEY}&query={query}",
        "series": f"https://api.themoviedb.org/3/search/tv?api_key={MOVIE_API_KEY}&query={query}",
        "toons": f"https://api.themoviedb.org/3/search/movie?api_key={MOVIE_API_KEY}&query={query}",
        "books": "",
        "anime": f"https://api.themoviedb.org/3/search/multi?api_key={MOVIE_API_KEY}&query={query}",
    }
    
    url = urls[media_type]
    if not url:
        return []
    
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    if data['results']:
        match media_type:
            case "series":
                for item in data['results']:
                    item['title'] = item.pop('name')
                    item['release_date'] = item.pop('first_air_date')
            case "books":
                pass
            case "anime":
                # output_list = [serie for serie in data['results'] if serie["media_type"]=="tv"]
                # data['results'] = output_list
                for item in data['results']:
                    if item["media_type"]=="tv":
                        item['title'] = item.pop('name')
                        item['release_date'] = item.pop('first_air_date')
        # print(data['results'][0])
        
        return data['results']#[0]  # change to make possible for seeing all possible results
    return []

def index(request, slug="films"):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    form = MediaItemForm()
    error = None

    # ✅ Handle deletion
    if request.method == "POST" and "delete_movie_id" in request.POST:
        # print(request.POST)
        media_id = request.POST.get("delete_movie_id")
        try:
            item = MediaItem.objects.get(id=media_id, user=user)
            item.delete()
        except MediaItem.DoesNotExist:
            pass  # optionally show a message
        return redirect('rating_menu')  # Refresh the page

    # ✅ Handle form submission
    if request.method == "POST":
        if "media_type" in request.POST:
            slug = request.POST.get("media_type")
            return redirect('rating_menu', slug=slug)

        else:
            form = MediaItemForm(request.POST)
            if form.is_valid():
                
                title = form.cleaned_data['title']
                rating = form.cleaned_data['rating']
                try:
                    movie_data = search_media_tmdb(title, slug)[0]#A problem if the result is None
                    if movie_data:
                        with transaction.atomic():
                            MediaItem.objects.create(
                                user=user,
                                title=movie_data['title'],
                                description=movie_data['overview'],
                                poster_url="https://image.tmdb.org/t/p/w500" + movie_data['poster_path'],
                                rating=int(rating),
                                tmdb_id=movie_data['id'],
                                genre = movie_data['genre_ids'],
                                year = datetime.datetime.strptime(movie_data['release_date'], "%Y-%m-%d"),
                                type = slug,
                            )
                            form = MediaItemForm()  
                    else:
                        error = "Film doest exist in TMDB database."
                except Exception as e:
                    error = f"Save error: {str(e)}"
            else:
                error = "form error."
        suggestion = request.POST.get("suggestion")
        print(suggestion)
        if suggestion:
            movie_list = MediaItem.objects.filter(user=request.user, type=slug, title=suggestion)
        else:
                movie_list= MediaItem.objects.filter(user=user, type=slug).order_by('-created_at')
    else:
        movie_list= MediaItem.objects.filter(user=user, type=slug).order_by('-created_at')
        
    if request.method == "GET" and "q" in request.GET:
        query = request.GET.get("q")
        suggestions = search_media_tmdb(query, slug)
            
        if suggestions:
            # print(suggestions[:6])
            return render(request, "rating_menu/index.html", {
            "suggestions": suggestions
    })
    if request.method == "GET" and "title" in request.GET:
        
        query = request.GET.get("title")
        suggestions = search_media_tmdb(query, slug)
        if "title" in request.GET:
            return JsonResponse({
            "suggestions": suggestions,
            "first_title": suggestions[0]["title"],
            "image": suggestions[0]["poster_path"]
            })
    
    
    # PAGINATOR: Show 10 movies per page
    paginator = Paginator(movie_list, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "rating_menu/index.html", {
        "page_obj": page_obj,
        "movie_titles": [movie.title for movie in movie_list],
        "form": form,
        "error": error,
        "slug": slug
    })
    

