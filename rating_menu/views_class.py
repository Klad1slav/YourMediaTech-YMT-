# from django.shortcuts import render, redirect,  get_object_or_404
# from django.db import transaction
# from .forms import MediaItemForm 
# from .models import MediaItem
# from django.conf import settings
# import requests
# import datetime
# from django.core.paginator import Paginator
# from django.http import JsonResponse
# from django.views import View

# def search_game_rawg(query):
#     RAWG_API_KEY = settings.RAWG_API_KEY
#     url = f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&search={query}"
    
#     response = requests.get(url)
#     if response.status_code != 200:
#         return []

#     data = response.json()
#     results = data.get('results', [])
#     if not results:
#         return []

#     game = results[0] # Take the first result
#     slug = game['slug']

#     details_url = f"https://api.rawg.io/api/games/{slug}?key={RAWG_API_KEY}"
#     details_response = requests.get(details_url)
#     if details_response.status_code != 200:
#         return []

#     game_details = details_response.json()

#     return {
#         'title': game_details.get('name'),
#         'overview': game_details.get('description_raw'), #change to overview
#         'poster_url': game_details.get('background_image'),
#         'release_date': game_details.get('released'),
#         'id': game_details.get('id'),
#         'genre': [g['name'] for g in game_details.get('genres', [])]
#     }
    
# def search_book_open_library(query):
#     url = f"https://openlibrary.org/search.json?q={query}"
    
#     response = requests.get(url)
#     data = response.json()

    
#     if response.status_code != 200:
#         return []

#     data = response.json()
#     if data['docs']:
#         book = data['docs'][0]

#         key = f"https://openlibrary.org/{book['key']}.json"
#         response = requests.get(key)
#         work = response.json()
        
#         print(book['title'])
#         print(work['description'])
#         print(f'https://covers.openlibrary.org/b/id/{book['cover_i']}.jpg')
#         print(work['first_publish_date'])
#         print([g for g in work.get('subjects', [])[:5]])

#         if  book['cover_i']:
#             poster_url = f'https://covers.openlibrary.org/b/id/{book['cover_i']}.jpg'
#         else:
#             poster_url = "https://www.vectorstock.com/royalty-free-vectors/404-page-not-found-vectors"
        
#         return {
#             'title': book['title'],
#             'overview': work['description'],
#             'poster_url':  f'https://covers.openlibrary.org/b/id/{book['cover_i']}.jpg',
#             'release_date': work['first_publish_date'],
#             'genre': [g for g in work.get('subjects', [])[:5]]
#             }
#     return []

# def search_media_tmdb(query, media_type)->list:
#     MOVIE_API_KEY = settings.TMDB_API_KEY
#     urls = {
#         "films": f"https://api.themoviedb.org/3/search/movie?api_key={MOVIE_API_KEY}&query={query}",
#         "series": f"https://api.themoviedb.org/3/search/tv?api_key={MOVIE_API_KEY}&query={query}",
#         "toons": f"https://api.themoviedb.org/3/search/movie?api_key={MOVIE_API_KEY}&query={query}",
#         "anime": f"https://api.themoviedb.org/3/search/multi?api_key={MOVIE_API_KEY}&query={query}",
#     }
    
#     url = urls[media_type]
#     if not url:
#         return []
    
#     response = requests.get(url)
#     if response.status_code != 200:
#         return []

#     data = response.json()
#     if data['results']:
#         match media_type:
#             case "series":
#                 for item in data['results']:
#                     item['title'] = item.pop('name')
#                     item['release_date'] = item.pop('first_air_date')
#             case "anime":
#                 for item in data['results']:
#                     if item["media_type"]=="tv":
#                         item['title'] = item.pop('name')
#                         item['release_date'] = item.pop('first_air_date')
#         return data['results']#[0]  # change to make possible for seeing all possible results
#     return []


# class IndexView(View):
#     template_name = "rating_menu/index.html"

#     def get(self, request, slug="films"):
#         if not request.user.is_authenticated:
#             return redirect('login')

#         # ✅ Show suggestions in modal window
#         if "q" in request.GET:
#             return self.show_suggestions_modal(slug, request.GET.get("q"), request)

#         if "title" in request.GET:
#             return self.shirt_description_modal(slug, request.GET.get("title"))

#         # ✅ Give the media/suggestions list
#         suggestion = request.GET.get("suggestion")
#         if suggestion:
#             movie_list = MediaItem.objects.filter(user=request.user, type=slug, title=suggestion)
#         else:
#             movie_list = MediaItem.objects.filter(user=request.user, type=slug).order_by('-created_at')

#         # ✅ PAGINATOR: Show 10 movies per page
#         paginator = Paginator(movie_list, 10)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

#         form = MediaItemForm()
#         return render(request, self.template_name, {
#             "page_obj": page_obj,
#             "movie_titles": [movie.title for movie in movie_list],
#             "form": form,
#             "slug": slug
#         })

#     def post(self, request, slug="films"):
#         if not request.user.is_authenticated:
#             return redirect('login')

#         user = request.user
#         form = MediaItemForm(request.POST)

#         # ✅ Handle deletion
#         if "delete_movie_id" in request.POST:
#             self.delete_media_piece(request.POST.get("delete_movie_id"), user)

#         # ✅ Redirect to chosen section
#         if "media_type" in request.POST:
#             slug = request.POST.get("media_type")
#             return redirect('rating_menu', slug=slug)

#         # ✅ Handle form submission
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             rating = form.cleaned_data['rating']
#             self.create_media_item(user, title, rating, slug)
#         else:
#             error = "form error."

#         # Re-render the page after POST
#         return self.get(request, slug)

#     def show_suggestions_modal(self, slug, query, request):
#         match slug:
#             case "films" | "series" | "toons" | "anime":
#                 suggestions = search_media_tmdb(query, slug)
#             case "games":
#                 suggestions = search_game_rawg(query)
#             case "books":
#                 suggestions = search_book_open_library(query)
#             case _:
#                 suggestions = []

#         if suggestions:
#             return render(request, self.template_name, {
#                 "suggestions": suggestions
#             })
#         else:
#             return JsonResponse({"error": "No suggestions found."})

#     def shirt_description_modal(self, slug, query):
#         match slug:
#             case "films" | "series" | "toons" | "anime":
#                 suggestions = search_media_tmdb(query, slug)
#                 if suggestions:
#                     return JsonResponse({
#                         "suggestions": suggestions,
#                         "first_title": suggestions[0].get("title", "Unknown Title"),
#                         "image": suggestions[0].get("poster_url", "No Image Available")
#                     })
#             case "games":
#                 suggestions = search_game_rawg(query)
#             case "books":
#                 suggestions = search_book_open_library(query)
#             case _:
#                 suggestions = []

#         if suggestions:
#             return JsonResponse({
#                 "suggestions": suggestions,
#                 "first_title": suggestions[0].get("title", "Unknown Title"),
#                 "image": suggestions[0].get("poster_url", "No Image Available")
#             })
#         else:
#             return JsonResponse({
#                 "error": "No suggestions found.",
#                 "suggestions": []
#             })

#     def delete_media_piece(self, query, user):
#         media_id = query
#         try:
#             item = MediaItem.objects.get(id=media_id, user=user)
#             item.delete()
#         except MediaItem.DoesNotExist:
#             pass

#     def create_media_item(self, user, title, rating, slug):
#         match slug:
#             case "films" | "series" | "toons" | "anime":
#                 media_data = search_media_tmdb(title, slug)[0]
#                 release_date = datetime.datetime.strptime(media_data['release_date'], "%Y-%m-%d")
#                 poster_url = "https://image.tmdb.org/t/p/w500" + media_data['poster_path']
#                 genre = media_data['genre_ids']
#             case "games":
#                 media_data = search_game_rawg(title)
#                 release_date = datetime.datetime.strptime(media_data['release_date'], "%Y-%m-%d") if media_data['release_date'] else None
#                 poster_url = media_data['poster_url']
#                 genre = media_data['genre']
#             case "books":
#                 media_data = search_book_open_library(title)
#                 release_date = datetime.datetime.strptime(media_data['release_date'], "%B, %Y") if media_data['release_date'] else None
#                 poster_url = media_data['poster_url']
#                 genre = media_data['genre']

#         try:
#             if media_data:
#                 with transaction.atomic():
#                     MediaItem.objects.create(
#                         user=user,
#                         title=media_data['title'],
#                         description=media_data['overview'],
#                         poster_url=poster_url,
#                         rating=int(rating),
#                         genre=genre,
#                         year=release_date,
#                         type=slug,
#                     )
#         except Exception as e:
#             print(f"Save error: {str(e)}")