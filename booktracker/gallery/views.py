from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from gallery.models import Book, UserGallery
from django.db.models import Q
import random

# Create your views here.
class BookForm(forms.ModelForm):
    """Klasse zur Formularerstellung."""

    class Meta:
        model = Book
        fields = ['titel', 'autor', 'buchcover', 'seitenanzahl', 'beschreibung', 'erscheinungsdatum', 'sprache',
                  'kategorie']
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def overview(request):
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()
    all_books = Book.objects.all()
    user_gallery_data = {}

    books = list(all_books)
    random.shuffle(books)
    empfohlene_buecher = list(all_books)
    random.shuffle(empfohlene_buecher)
    empfohlene_buecher = empfohlene_buecher[:3]

    if search_query:
        all_books = all_books.filter(
            Q(titel__icontains=search_query) | Q(autor__icontains=search_query)
        )

    if category_filter:
        all_books = all_books.filter(kategorie=category_filter)

    if request.user.is_authenticated:
        # Finde für jedes Buch den Fortschritt des aktuellen Nutzers
        for book in all_books:
            user_gallery = UserGallery.objects.filter(user=request.user, book=book).first()
            user_gallery_data[book.id] = user_gallery

    return render(request, 'basic/overview.html', {
        'books': books,
        'user_gallery_data': user_gallery_data,
        'today': now(),
        'search_query': search_query,
        'selected_category': category_filter,
        'empfohlene_buecher': empfohlene_buecher,
    })

@login_required
def user_settings(request):
    return render(request, 'basic/settings.html')

@login_required
def profile(request):
    user = request.user
    gelesene_buecher = UserGallery.objects.filter(user=user, tracker="Gelesen")
    begonnene_buecher = UserGallery.objects.filter(user=user, tracker="Begonnen")
    geplante_buecher = UserGallery.objects.filter(user=user, tracker="Geplant")

    if request.method == "POST":
        name = request.POST.get("name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if name:
            user.first_name = name
        if email:
            user.email = email
        if last_name:
            user.last_name = last_name

        user.save()
        return redirect("profile")

    return render(request, 'basic/profile.html', {
        'user': user,
        'gelesene_buecher': gelesene_buecher,
        'begonnene_buecher': begonnene_buecher,
        'geplante_buecher': geplante_buecher,
    })

@login_required
def upload(request, pk=None):
    if pk:
        book = get_object_or_404(Book, pk=pk)
    else:
        book = Book()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('/')
    else:
        form = BookForm(instance=book)
    return render(request, 'basic/upload.html', {'form': form})

@login_required
def update_progress(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_gallery, created = UserGallery.objects.get_or_create(user=request.user, book=book)

    if request.method == 'POST':
        tracker = request.POST.get('tracker')
        begonnen = request.POST.get('begonnen')
        fortschritt = request.POST.get('fortschritt')
        bewertung = request.POST.get('bewertung')
        inhaltsfokus = request.POST.get('inhaltsfokus')

        # Fortschrittslogik
        if tracker == "Geplant":
            user_gallery.tracker = "Geplant"
            user_gallery.begonnen = None
            user_gallery.fortschritt = None
            user_gallery.bewertung = None
            user_gallery.inhaltsfokus = None
        elif tracker == "Begonnen":
            user_gallery.tracker = "Begonnen"
            user_gallery.bewertung = None
            user_gallery.inhaltsfokus = None
            if begonnen:
                user_gallery.begonnen = begonnen
            if fortschritt:
                user_gallery.fortschritt = fortschritt
        elif tracker == "Gelesen":
            if not user_gallery.begonnen:
                user_gallery.begonnen = now().date()
            user_gallery.tracker = "Gelesen"
            user_gallery.fortschritt = book.seitenanzahl
            if bewertung:
                user_gallery.bewertung = bewertung
            if inhaltsfokus:
                user_gallery.inhaltsfokus = inhaltsfokus
        elif tracker == "None":
            user_gallery.tracker = "None"
            user_gallery.begonnen = None
            user_gallery.fortschritt = None
            user_gallery.bewertung = None
            user_gallery.inhaltsfokus = None
        user_gallery.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('overview')
