from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic
import logging
from .restcalls import *

# Get an instance of a logger
logger = logging.getLogger(__name__)

base_lyric_service_url = "https://dummy.restapiexample.com/api/v1/employee/"

# Create your views here.
def get_concert_list_view(request):
    if request.method == "GET":
      # The context/data to be presented in the HTML template
      context = generate_concert_context(request)
      # Render a HTML page with specified template and context
      return render(request, 'concert/concert_list.html', context)


def check_is_registrated(user, concert):
    is_registrated = False
    if user.id is not None:
        # Check if user enrolled
        concert_counts = Registration.objects.filter(user=user, concert=concert).count()
        if concert_counts > 0:
            is_registrated = True
    return is_registrated


def generate_concert_context(request):
    context = {}
    concerts = Concert.objects.order_by('-total_registrations')[:30]
    for concert in concerts:
        current_user = request.user
        if current_user.is_authenticated:
            concert.is_registrated = check_is_registrated(current_user, concert)
    context['concert_list'] = concerts
    return context


def register(request, concert_id):
    concert = get_object_or_404(Concert, pk=concert_id)
    user = request.user
    is_enrolled = check_is_registrated(user, concert)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Registration.objects.create(user=user, concert=concert)
        concert.total_registrations += 1
        concert.save()

    return HttpResponseRedirect(reverse(viewname='concert:details', args=(concert.id,)))


class ConcertDetailView(generic.DetailView):
    model = Concert
    template_name = 'concert/concert_detail_bootstrap.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        concert_id = self.kwargs['pk']
        concert = Concert.objects.get(pk=concert_id)
        for song in concert.songs.all():
            lyrics = get_lyrics(base_lyric_service_url, song.pk)
            print(lyrics)
            song.lyrics = lyrics
            song.save()
        context['concert'] = concert
        return context

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'concert/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("concert:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'concert/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('concert:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'concert/user_login_bootstrap.html', context)
    else:
        return render(request, 'concert/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('concert:index')