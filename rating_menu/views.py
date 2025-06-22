from django.shortcuts import render
from .forms import MediaItemForm  # Make sure the name matches your forms.py

def index(request):
    form = MediaItemForm()
    success = False
    if request.method == 'POST':
        form = MediaItemForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = MediaItemForm()  # Reset the form after saving
    return render(request, "rating_menu/index.html", {'form': form, 'success': success})
