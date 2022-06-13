import email
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.http import HttpResponse


def login_user(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=email)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            # This creates a session in the database and the browser of the user.
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username or password is not correct!')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid:
            try:
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
            except ValueError:
                messages.error(request, "Data didn't validate!. ValueError!")
        else:
            messages.error(request, 'An error occured during registration.')

    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    topics = Topic.objects.all()[0:5]  # Show the first five topics only.
    # q will be part of the url in the address bar when the user clicks on some category e.g., q=Python in http://127.0.0.1:8000/?q=Python
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # We can search roomb by topic, room name or room description
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )  # i in icontains make it case insensitive. When q is an empty string '' it will return all Rooms without any filtering.

    # Retrieve messages and filter them by the topic and name of the room. If All topic is selected then show all messages.
    messages_posted = Message.objects.filter(Q(room__topic__name__icontains=q))
    # To find the length of a queryset we use count() which functions faster than len() in Python.
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'messages_posted': messages_posted}
    return render(request, 'base/home.html', context)


def room(request, pk):  # pk is the primary key of a chat room.
    room = Room.objects.get(id=pk)
    # Give us all the messages in this room. message_set contains the class Message before the underscore but with a lower case m.
    # Show messages in descending order. - is for descending order.
    room_messages = room.message_set.all().order_by('-created')

    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # This guy is sending a message, so he has joined the list of participants. Add her/him.
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def retrieve_user_profile(request, pk):
    user = User.objects.get(id=pk)
    # We can get the children of a scpecific object by modelNameStartingWithSmallLetter.set.all()/filter()
    rooms = user.room_set.all()
    messages_posted = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'messages_posted': messages_posted, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        # Created will be False if the topic is already in the database otherwise True.
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        # print(request.POST)
        # form = RoomForm(request.POST)
        # if form.is_valid:
        #     room = form.save(commit=False)
        #     # Set the current logged in user who is creating the room as the room host.
        #     room.host = request.user
        #     room.save()
        # home refers to the name in path('', views.home, name="home") in module urls.py
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed this action!")
    if request.method == 'POST':
        room.delete()  # This will delete the room from the database.
        # home refers to the name in path('', views.home, name="home") in module urls.py
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed to delete a message that you have not written.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html')


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def show_topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # http://127.0.0.1:8000/?q=Python will filter topics by 'Python'
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def show_activities_page(request):
    messages_posted = Message.objects.all()
    return render(request, 'base/activity.html', {'messages_posted': messages_posted})
