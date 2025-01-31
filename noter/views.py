from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime
from .models import List, Note
from django.contrib import messages
from django.views.decorators.cache import cache_control
from datetime import date, datetime

@login_required
def Home(request):
    # if request.method == 'POST':
    ulists = List.objects.filter(user = request.user)
    lists = []
    list_id = 0
    for list in ulists:
        if list.name != "Today":
            lists.append(list)
        if list.name == "Today":
            list_id = list.id
    unotes = Note.objects.filter(user = request.user)
    notes = []
    today = date.today()
    for note in unotes:
        if note.end_at <= today and note.status == False:
            if note.end_at:
                note.end_at = note.end_at.strftime('%Y-%m-%dT%H:%M')
            if note.start_at:
                note.start_at = note.start_at.strftime('%Y-%m-%dT%H:%M')
            if note.deadline:
                note.deadline = note.deadline.strftime('%Y-%m-%dT%H:%M')
            notes.append(note)

    return render(request, 'noter/home.html', {'lists': lists, 'number_of_notes':len(notes), 'notes':notes, 'list_id': list_id, 'today': today, 'none': None})
    
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
def CreateList(request, list_id):
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
        if list_id!=0:
            return redirect(reverse('noter:lists', args=[list_id]))
        return redirect('/noter/')
    

#every list show view
@login_required
def ShowList(request, list_id):
    name = List.objects.get(id = list_id)
    ulists = List.objects.filter(user = request.user)
    unotes = Note.objects.filter(user = request.user, list = name, status = False)
    done_notes = []
    today = date.today()
    for note in unotes:
        if note.end_at <= today and note.status == False:
            if note.end_at:
                note.end_at = note.end_at.strftime('%Y-%m-%dT%H:%M')
            if note.start_at:
                note.start_at = note.start_at.strftime('%Y-%m-%dT%H:%M')
            if note.deadline:
                note.deadline = note.deadline.strftime('%Y-%m-%dT%H:%M')
            done_notes.append(note)
    number_of_notes = len(done_notes)
    return render(request, 'noter/lists.html', {'done_notes': done_notes, 'name': name,'list_id':list_id, 'lists': ulists, 'number_of_notes': number_of_notes})
    
#note
@login_required
def CreateNote(request):
    if request.method == 'POST':
        title = request.POST.get('title_input')
        create_at = datetime.now()
        user = request.user
        description = None
        list1 = None
        start_at = None
        end_at = None
        deadline_at = None

        description_text = request.POST.get('description_input')
        if description_text:
            description = description_text

        list_id2 = request.POST.get('select_input')
        if list_id2:
            list1 = List.objects.get(id=list_id2)

        datetime_str = request.POST.get('start_at')
        if datetime_str:
            start_at = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

        datetime_str = request.POST.get('end_at')
        if datetime_str:
            end_at = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        else:
            end_at = datetime.now()

        datetime_str = request.POST.get('deadline_at')
        if datetime_str:
            deadline_at = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

        note_data = {
            "title": title,
            "user": request.user,
            "created_at": create_at,
            "start_at": start_at,
            "end_at": end_at,
            "deadline": deadline_at,
            "list": list1,
            "user": user,
            "description": description
        }
        note1 = Note.objects.create(**note_data)
        note1.save()
        return redirect(reverse(f'noter:home'))
    



@login_required
def CreateNoteList(request, list_id):
    if request.method == 'POST':
        title = request.POST.get('title_input')
        create_at = datetime.now()
        user = request.user
        description = None
        list1 = None
        start_at = None
        end_at = None
        deadline_at = None

        description_text = request.POST.get('description_input')
        if description_text:
            description = description_text

        list1 = List.objects.get(id=list_id)

        datetime_str = request.POST.get('start_at')
        if datetime_str:
            start_at = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

        datetime_str = request.POST.get('end_at')
        if datetime_str:
            end_at = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        else:
            end_at = datetime.now()

        datetime_str = request.POST.get('deadline_at')
        if datetime_str:
            deadline_at = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

        note_data = {
            "title": title,
            "user": request.user,
            "created_at": create_at,
            "start_at": start_at,
            "end_at": end_at,
            "deadline": deadline_at,
            "list": list1,
            "user": user,
            "description": description
        }
        note1 = Note.objects.create(**note_data)
        note1.save()
    return redirect(reverse('noter:lists', args=[list_id]))









    
@login_required
def update(request, note_id, list_id):
    note = Note.objects.get(id = note_id)
    if request.method == 'POST':
        u_name = request.POST.get('u_name')
        if u_name:
            note.title = u_name

        u_description = request.POST.get('u_description')
        if u_description:
            note.description = u_description

        u_start_at = request.POST.get('u_start_at')
        if u_start_at:
            note.start_at = datetime.strptime(u_start_at, '%Y-%m-%dT%H:%M')

        u_end_at = request.POST.get('u_end_at')
        if u_end_at:
            note.end_at = datetime.strptime(u_end_at, '%Y-%m-%dT%H:%M')

        u_deadline = request.POST.get('u_deadline')
        if u_deadline:
            note.deadline = datetime.strptime(u_deadline, '%Y-%m-%dT%H:%M')

        u_list_id = request.POST.get('u_list_id')
        if u_list_id:
            note.list = List.objects.get(id = u_list_id)
        note.save()
        if list_id != 0:
            return redirect(reverse('noter:lists', args=[list_id]))
        return redirect(f'noter:home')

@login_required
def do(request, note_id, list_id):
    note = Note.objects.get(id=note_id)
    if request.method == 'POST':
        note.status = not note.status
        note.save()
        if list_id != 0:
            return redirect(reverse('noter:lists', args=[list_id]))
        return redirect(f'noter:home')
    
@login_required
def delete(request, note_id, list_id):
    note = Note.objects.get(id=note_id)
    if request.method == 'POST':
        note.delete()
        if list_id != 0:
            return redirect(reverse('noter:lists', args=[list_id]))
        return redirect(f'noter:home')

@login_required
def History(request):
    return render(request, 'noter/history.html')