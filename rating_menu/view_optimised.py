from django.shortcuts import render, redirect
from django.db import transaction
from .forms import MediaItemForm 
from .models import MediaItem
from django.conf import settings
import requests
import datetime
from django.core.paginator import Paginator
from django.http import JsonResponse

def search_media(query, media_type)->list:
    MOVIE_API_KEY = settings.TMDB_API_KEY
    RAWG_API_KEY = settings.RAWG_API_KEY
    GOOGLE_API_KEY = "AIzaSyAUHG9KP3gl1-z0VHdWZV5E6D1v6Bwbq-M"  
    
    urls = {
        "films": f"https://api.themoviedb.org/3/search/movie?api_key={MOVIE_API_KEY}&query={query}",
        "series": f"https://api.themoviedb.org/3/search/tv?api_key={MOVIE_API_KEY}&query={query}",
        "toons": f"https://api.themoviedb.org/3/search/movie?api_key={MOVIE_API_KEY}&query={query}",
        "anime": f"https://api.themoviedb.org/3/search/multi?api_key={MOVIE_API_KEY}&query={query}",
        "games": f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&search={query}",
        "books": f"https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict=en&akey={GOOGLE_API_KEY}"
    }
    url = urls[media_type]
    if not url:
        return []

    response = requests.get(url)
    if response.status_code != 200:
        print(response.status_code)
        return []
    
    data = response.json()
    if media_type == "books":
        results = data.get('items', [])[:5]   
    else: 
        results = data.get('results', [])[:5]
    
    if not results:
        return []
    try:
        match media_type:
            case "series":
                for item in results:
                    item['title'] = item.pop('name')
                    item['release_date'] = item.pop('first_air_date')
            case "anime":
                for item in results:
                    if item["media_type"]=="tv":
                        item['title'] = item.pop('name')
                        item['release_date'] = item.pop('first_air_date')
            case "games":
                for item in results:
                    item['title'] = item.pop('name')
                    item['poster_path'] = item.pop('background_image')
                    item['release_date'] = item.pop('released')
                    item['genre'] = [g['name'] for g in item.get('genres', [])]
            case "books":
                for item in results:
                    item['title'] = item['volumeInfo'].get('title', '')
                    item['overview'] = item['volumeInfo'].get('description', '')
                    item['poster_path'] = item['volumeInfo']['imageLinks'].get('thumbnail', '')
                    item['genre'] = item['volumeInfo'].get('categories', '')
                    item['release_date'] = item['volumeInfo'].get('publishedDate', '')
        return results
    except Exception as e:
        error = f"Search error: {str(e)}"
    return error #type:ignore

def delete_media_piece(querry, user):
    media_id = querry
    try:
        item = MediaItem.objects.get(id=media_id, user = user)
        item.delete()
    except MediaItem.DoesNotExist:
        pass

def create_media_item(user, title, rating, slug):
    
    RAWG_API_KEY = settings.RAWG_API_KEY
    media_data = search_media(title, slug)[0]
    try:
        release_date = datetime.datetime.strptime(media_data['release_date'], "%Y-%m-%d")
    except Exception as e:
        release_date = datetime.datetime.strptime(media_data['release_date'], "%Y")
        
    
    match slug:
        case "films" | "series" | "toons" | "anime":
            genre = media_data['genre_ids']
            poster_url = "https://image.tmdb.org/t/p/w500" + media_data['poster_path']
        case "games":
            
            details_url = f"https://api.rawg.io/api/games/{media_data['id']}?key={RAWG_API_KEY}"
            details_response = requests.get(details_url)
            
            if details_response.status_code != 200:
                return []
            poster_url = media_data['poster_path']
            media_data['overview'] = details_response.json()['description_raw']
            genre = media_data['genre']# type: ignore
        case "books":
            poster_url = media_data['poster_path']# type: ignore
            genre = media_data['genre']# type: ignore
    print(media_data)
    try:
        if media_data:# type: ignore
            with transaction.atomic(): #whether full success or full fail
                MediaItem.objects.create(
                    user=user,
                    title=media_data['title'], # type: ignore
                    description=media_data['overview'], # type: ignore
                    poster_url=poster_url, # type: ignore
                    rating=int(rating),
                    # tmdb_id=game_data['id'],  # use as unique ID # type: ignore
                    genre=genre, # type: ignore
                    year= release_date, # type: ignore
                    type=slug,
                    )
            return
        else:
            error = "Media doesn't exist in database."
    except Exception as e:
        error = f"Save error: {str(e)}"
    return error #type:ignore

def show_suggestions_modal(slug, querry, request):
    match slug:
        case "films" | "series" | "toons" | "anime" | "games" | "books":
            suggestions = search_media(querry, slug)
        case _:
            suggestions = []
    if suggestions:  # Ensure suggestions is not None or empty
        return render(request, "rating_menu/index.html", {
            "suggestions": suggestions
        })
    else:
        return JsonResponse({"error": "No suggestions found."})
            
def shirt_description_modal(slug, querry):
    try:
        suggestions = search_media(querry, slug)
    except Exception as e:
        error = f"Search error: {str(e)}"
        return error #type:ignore
    match slug:
        case "films" | "series" | "toons" | "anime":
            suggestions[0]['poster_path'] = "https://image.tmdb.org/t/p/w300" + suggestions[0]['poster_path']
            

    if suggestions:
        return JsonResponse({
            "suggestions": suggestions,
            "first_title": suggestions[0].get("title", "Unknown Title"),
            "image": suggestions[0].get("poster_path", "No Image Available")
        })
    else:
            return JsonResponse({
            "error": "No suggestions found.",
            "suggestions": []
        })

def index(request, slug="films"):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    form = MediaItemForm(request.POST)
    error = None
    movie_list= MediaItem.objects.filter(user=user, type=slug).order_by('-created_at')
    
    # def post()
    if request.method == "POST": 
        # ✅ Handle deletion
        if "delete_movie_id" in request.POST:
            delete_media_piece(request.POST.get("delete_movie_id"), user)
        
        # ✅ Redirect to chosen section
        if "media_type" in request.POST:
            slug = request.POST.get("media_type")
            return redirect('rating_menu', slug=slug)
        
        # ✅ Give the media/suggestions list        
        if "suggestion" in request.POST:
            suggestion = request.POST.get("suggestion")
            movie_list = MediaItem.objects.filter(user=request.user, type=slug, title=suggestion)
            
        # ✅ Handle form submission
        if form.is_valid():
            title = form.cleaned_data['title']
            rating = form.cleaned_data['rating']
            create_media_item(user, title,rating,slug)
        else:
            error = "form error."
            
    # def get()
    if request.method == "GET":
        # ✅ Show suggestions in modal window
        if "q" in request.GET:
            return show_suggestions_modal(slug, request.GET.get("q"), request)
            
        if "title" in request.GET:
            return shirt_description_modal(slug, request.GET.get("title"))

    # ✅ PAGINATOR: Show 10 movies per page
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
    
