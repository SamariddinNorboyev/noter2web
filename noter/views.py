from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime
from .models import List, Note
from django.contrib import messages
from django.views.decorators.cache import cache_control

@login_required
def Home(request):
    # if request.method == 'POST':
    lists = List.objects.filter(user = request.user)
    return render(request, 'noter/home.html', {'lists': lists})
    
@login_required
def Upcoming(request):
    # if request.method == 'POST':
    return render(request, 'noter/upcoming.html')
    
@login_required
def StickyWall(request):
    # if request.method == 'POST':
    return render(request, 'noter/stickywall.html')    
    
@login_required
def Calendar(request):
    # if request.method == 'POST':
    return render(request, 'noter/calendar.html')



#list
@login_required
def CreateList(request):
    if request.method == 'POST':
        name = request.POST.get('list_name')
        color = request.POST.get('list_color')

        lists = List.objects.filter(user = request.user)
        for list in lists:
            if list.name == name:
                messages.error(request, (f'There is a list with name {name}'))
                return redirect('/noter/')
        if color == '':
            list1 = List(name = name, user = request.user)
            list1.save()
            return redirect('/noter/')
        list1 = List(name = name, color = color, user = request.user)
        list1.save()
        return redirect('/noter/')
    
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ShowList(request, list_id):
    name = List.objects.get(id = list_id)
    notes = Note.objects.filter(list = name)
    done = notes.filter(status = True)
    undone = notes.filter(status = False)
    return render(request, 'noter/lists.html', {'done_notes': done,'undone_notes':undone, 'name': name, 'list_id':list_id})
    
#note
@login_required
def CreateNote(request, list_id):
    if request.method == 'POST':
        title = request.POST.get('note_title')
        description = request.POST.get('note_description')
        list1 = List.objects.get(id = list_id)
        note1 = Note(title = title, description = description, list = list1)
        note1.save()
        return redirect(f'/noter/lists/{list_id}')
    
@login_required
def do(request, list_id, note_id):
    note = Note.objects.get(id=note_id)
    if request.method == 'POST':
        note.status = not note.status
        note.save()
        return redirect(f'/noter/lists/{list_id}')


        # return redirect('noter:lists', list_id=list_id)


        # response = redirect('noter:lists', list_id=list_id)
        # response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        # response['Pragma'] = 'no-cache'
        # return response

        # url = reverse('noter:lists', kwargs={'list_id': list_id})
        # return redirect(url)