from django.shortcuts import render, redirect
from django.db import transaction
from .forms import MediaItemForm 
from .models import MediaItem
from django.conf import settings
import requests
import datetime
import json

def search_media_tmdb(query, media_type):
    API_KEY = settings.TMDB_API_KEY
    urls = {
        "films": f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}",
        "series": f"https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&query={query}",
        "toons": "",
        "books": "",
        "games": "",
        "anime": "",
    }
    
    url = urls[media_type]
    response = requests.get(url)
    data = response.json()
    if data['results']:
        match media_type:
            # case "films":
            #     pass
            case "series":
                output_list = [serie for serie in data['results'] if serie["media_type"]=="tv"]
                data['results'] = output_list
                for item in data['results']:
                    item['title'] = item.pop('name')
                    item['release_date'] = item.pop('first_air_date')
            case "toons":
                pass
            case "books":
                pass
            case "games":
                pass
            case "anime":
                pass
        print(data['results'][0])
        
        return data['results'][0]  # change to make possible for seeing all possible results
    return None

def index(request, slug="films"):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    form = MediaItemForm()
    error = None
    
    # if request.method == "GET":
    #     if "suggestion" in request.GET:
    #         title  = request.GET.get("suggestion")
    #         movies = MediaItem.objects.filter(user=user, type = slug, title=title)
    #         print(request.GET)
    #         return render(request, "rating_menu/index.html", {
    #             "movies": movies,
    #             "movie_titles": [movie.title for movie in movies],
    #             "form": form,
    #             "error": error,
    #             "slug": slug
    #         })
    if request.method == "POST":
        if "media_type" in request.POST:
            slug = request.POST.get("media_type")
            return redirect('rating_menu', slug=slug)

        else:
            form = MediaItemForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                try:
                    movie_data = search_media_tmdb(title, slug)
                    if movie_data:
                        with transaction.atomic():
                            MediaItem.objects.create(
                                user=user,
                                title=movie_data['title'],
                                description=movie_data['overview'],
                                poster_url="https://image.tmdb.org/t/p/w500" + movie_data['poster_path'],
                                rating=movie_data['vote_average'],
                                tmdb_id=movie_data['id'],
                                genre = movie_data['genre_ids'],
                                year = datetime.datetime.strptime(movie_data['release_date'], "%Y-%m-%d"),
                                type = slug                      
                            )
                            form = MediaItemForm()  
                    else:
                        error = "Film doesn't exist in TMDB database."
                except Exception as e:
                    error = f"Save error: {str(e)}"
            else:
                error = "form error."
        suggestion = request.POST.get("suggestion")
        if suggestion:
            movies = MediaItem.objects.filter(user=request.user, type=slug, title=suggestion)
        else:
            movies = MediaItem.objects.filter(user=request.user, type=slug)
    else:
        movies = MediaItem.objects.filter(user=request.user, type=slug)
    print(request.POST)
    return render(request, "rating_menu/index.html", {
        "movies": movies,
        "movie_titles": [movie.title for movie in movies],
        "form": form,
        "error": error,
        "slug": slug
    })