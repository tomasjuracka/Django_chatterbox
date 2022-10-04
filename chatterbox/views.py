from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import ModelForm
# from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect

from chatterbox.models import Room, Message
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView


# Create your views here
def hello(request, s):
    return HttpResponse(f'Hello, {s} world!')


def home(request):
    rooms = Room.objects.all()  # searches for all rooms

    context = {'rooms': rooms}
    return render(request, 'chatterbox/home.html', context)


@login_required
def search(request):
    if request.method == 'POST':
        s = request.POST.get('search')
        s = s.strip()
        if len(s) > 0:
            rooms = Room.objects.filter (name__contains=s)
            messages = Message.objects.filter (body__contains=s)

            context = {'rooms': rooms, 'messages': messages, 'search': s}
            return render(request, 'chatterbox/search.html', context)
        else:
            context = {'rooms': None, 'messages': None}
            # return redirect ('home')
    return redirect('home')


# @login_required
"""
def search(request,s):
    rooms = Room.objects.filter(name__contains=s)
    response = "Rooms: "
    for room in rooms:
        response += room.name + ", "
    return HttpResponse(rooms)

    messages = Message.objects.filter(body__contains=s)
    response += "<br>Messages: "
    for message in messages:
        response += message.body[0:10] + " ... , "

    return render(request, "chatterbox/search.html", context)
"""


@login_required
def room(request, pk):
    room = Room.objects.get(id=pk)  # searches for room with selected id
    messages = Message.objects.filter(room=pk)  # selects all messages in chosen room

    # we have to process every new message
    if request.method == 'POST':
        file_url = ""
        if request.FILES.get('upload'):
            upload = request.FILES['upload']
            file_storage = FileSystemStorage()
            file = file_storage.save(upload.name, upload)
            file_url = file_storage.url(file)
        body = request.POST.get('body').strip()
        if len(body) > 0 or request.FILES.get('upload'):
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=body,
                file=file_url
            )
        return HttpResponseRedirect(request.path_info)

    context = {'room': room, 'messages': messages}
    return render(request, "chatterbox/room.html", context)


@login_required
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    if room.messages_count() == 0:
        room.delete()

        return redirect('rooms')

    context = {'room': room, 'message_count': room.messages_count()}
    return render(request, 'chatterbox/delete_room.html', context)


@login_required
def delete_room_yes(request, pk):
    room = Room.objects.get(id=pk)
    room.delete()
    return redirect('rooms')


@login_required
def rooms(request):
    rooms = Room.objects.all()

    context = {'rooms': rooms}
    return render(request, "chatterbox/rooms.html", context)


@login_required
def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        descr = request.POST.get('descr').strip()
        if len(name) > 0 and len(descr) > 0:
            room = Room.objects.create(
                host=request.user,
                name=name,
                description=descr
            )

            return redirect('room', pk=room.id)

    return render(request, 'chatterbox/create_room.html')

# Old room delete that purged room along with its content
# @login_required
# def delete_room(request, pk):
#     room = Room.objects.get(id=pk)
#     room.delete()
#
#     return redirect('rooms')


# form
class RoomEditForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


# view
@method_decorator(login_required, name='dispatch')
class EditRoom(UpdateView):
    template_name = 'chatterbox/edit_room.html'
    model = Room
    form_class = RoomEditForm
    success_url = reverse_lazy('rooms')

# @login_required
# def new_room(request):
#     if request.method == 'POST':
#         room = Room.objects.create(
#             name=request.POST.get('name'),
#             description=request.POST.get('descr')
#         )
#
#         return redirect('room', pk=room.id)
#
#     return redirect('home')
