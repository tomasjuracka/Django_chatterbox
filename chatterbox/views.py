from django.http import HttpResponse
from django.shortcuts import render

from chatterbox.models import Room, Message


# Create your views here.
def hello(request, s):
    return HttpResponse(f'Hello, {s} world!')


def home(request):
    rooms = Room.objects.all()  # najdeme všechny místnosti

    context = {'rooms': rooms}
    return render(request, 'chatterbox/home.html', context)

def search(request, s):
    rooms = Room.objects.filter(name__contains=s)
    # commented lines became redundant after implementing context (variable) at the end of page
    # response = "Rooms: "
    # for room in rooms:
    #    response += room.name + ", "

    messages = Message.objects.filter(body__contains=s)
    # response += "<br>Messages: "
    # for message in messages:
    #    response += message.body[0:10] + " ... , "

    context = {'rooms': rooms,
               'messages': messages}
    return render(request, "chatterbox/search.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=pk)

    context = {'room': room, 'messages': messages}
    return render(request, "chatterbox/room.html", context)
