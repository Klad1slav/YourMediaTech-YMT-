from django.shortcuts import render, redirect,  get_object_or_404
from django.db import transaction
from .forms import MediaItemForm 
from .models import MediaItem
from django.conf import settings
import requests

def search_movie_tmdb(query):
    API_KEY = settings.TMDB_API_KEY
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        return data['results'][0]  # Первый результат
    return None

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    form = MediaItemForm()
    error = None

    # ✅ Handle deletion
    if request.method == "POST" and "delete_movie_id" in request.POST:
        media_id = request.POST.get("delete_movie_id")
        try:
            item = MediaItem.objects.get(id=media_id, user=user)
            item.delete()
        except MediaItem.DoesNotExist:
            pass  # optionally show a message
        return redirect('rating_menu')  # Refresh the page

    # ✅ Handle form submission
    if request.method == "POST":
        form = MediaItemForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            rating = form.cleaned_data['rating']
            try:
                movie_data = search_movie_tmdb(title)
                if movie_data:
                    with transaction.atomic():
                        MediaItem.objects.create(
                            user=user,
                            title=movie_data['title'],
                            description=movie_data['overview'],
                            poster_url="https://image.tmdb.org/t/p/w500" + movie_data['poster_path'],
                            rating=int(rating),
                            tmdb_id=movie_data['id']
                        )
                        form = MediaItemForm()  
                else:
                    error = "Film doest exist in TMDB database."
            except Exception as e:
                error = f"Save error: {str(e)}"
        else:
            error = "form error."

    
    movies = MediaItem.objects.filter(user=user)
    return render(request, "rating_menu/index.html", {
        "movies": movies,
        "form": form,
        "error": error
    })
