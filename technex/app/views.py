from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from django.contrib.auth import logout
from django import forms
from django.forms.widgets import *
from technex.app.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404,\
    HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from simplejson import dumps
from httplib import HTTPResponse
from django.db.utils import IntegrityError

class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'username', 'password1', 'password2', 'email', 'contact', 'gender', 'college',)

class TeamRegistrationForm(forms.Form):
    team_name = forms.CharField(max_length=20, label='Team Name', required=True)
    user1 = forms.CharField(max_length=50, label='Team member 1 username', required=False)
    user2 = forms.CharField(max_length=50, label='Team member 2 username', required=False)
    user3 = forms.CharField(max_length=50, label='Team member 3 username', required=False)
    user4 = forms.CharField(max_length=50, label='Team member 4 username', required=False)
    user5 = forms.CharField(max_length=50, label='Team member 5 username', required=False)

class EventRegistrationForm(forms.Form):
    CHOICES = (
        ('Aerostruct', 'Aero-Struct'),
        ('Directors Cut', "Director's Cut"),
        ('Res Novae', 'Res Novae'),
        ('Brandaid', 'Brand Aid'),
        ('Aqua Combat', 'Aqua Combat'),
        ('Ventura', 'Ventura'),
        ('Biz-Wiz', 'Biz-Wiz'),
        ('Manthan', 'Manthan'),
        ('Innoventure', 'Innoventure'),
        ('Balvigyaan', 'Balvigyaan'),
        ('Goldbergs Alley', "Goldberg's Alley"),
        ('Optika', 'Optika'),
        ('I-Robot', 'I-Robot'),
        ('Dash n Trounce', 'Dash n Trounce'),
        ('Robowars', 'Robowars'),
        ('Modex', 'Modex'),
    )
    text = '<span style="text-decoration:underline" onclick="window.open(\'/registration/team\', \'Technex\', \'height=600,width=600,scrollbars=yes\');">Click here</span> for registering your team'
    team_name = forms.CharField(max_length=20, label='Team Name', help_text=text, required=True)
    events = forms.MultipleChoiceField(choices=CHOICES, label='Events', help_text="Press 'Ctrl' to select multiple events")

def index(request):
    #Registration Check
    error = False
    reg_success = False
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            reg_success = True
        else:
            error = True
    else:
        form = RegistrationForm()
    template_data = {
        'form': form,
        'error': error,
        'registration_successful': reg_success
    }
    
    #General Notifications
    general_notifs = GeneralNotification.objects.all()
    template_data['general_notifs'] = general_notifs
    
    return render_to_response('index.html', template_data, context_instance=RequestContext(request))

def team_registration(request):
    if request.method == "POST":
        form = TeamRegistrationForm(request.POST)
        if form.is_valid():         
            name = form.cleaned_data.get('team_name', None)
            user1 = user2 = user3 = user4 = user5 = None
            if form.cleaned_data.get('user1', None):
                user1 = get_object_or_404(UserProfile, username=form.cleaned_data.get('user1', None))
            if form.cleaned_data.get('user2', None):
                user2 = get_object_or_404(UserProfile, username=form.cleaned_data.get('user2', None))
            if form.cleaned_data.get('user3', None):
                user3 = get_object_or_404(UserProfile, username=form.cleaned_data.get('user3', None))
            if form.cleaned_data.get('user4', None):
                user4 = get_object_or_404(UserProfile, username=form.cleaned_data.get('user4', None))
            if form.cleaned_data.get('user5', None):
                user5 = get_object_or_404(UserProfile, username=form.cleaned_data.get('user5', None))
            
            try:
                team = Team.objects.create(name=name)
                if user1:
                    team.participants.add(user1.pk)
                if user2:
                    team.participants.add(user2.pk)
                if user3:
                    team.participants.add(user3.pk)
                if user4:
                    team.participants.add(user4.pk)
                if user5:
                    team.participants.add(user5.pk)
                template_data = {
                    'message': 'Registration successful. Congratulations! <span onclick="history.go(-2);">Click here</span> to go to event registrations.',
                }
                return render_to_response('registration/success.html', template_data, context_instance=RequestContext(request))
            except IntegrityError:
                form.errors['team_name'] = (("This team name already exists"),)

    else:    
        form = TeamRegistrationForm()
    
    template_data = {
        'form': form,
    }
    return render_to_response('registration/team_registration.html', template_data, context_instance=RequestContext(request))

def event_registration(request):
    if request.method == "POST":
        form = EventRegistrationForm(request.POST)
        if form.is_valid():         
            events = form.cleaned_data.get('events', None)
            team = get_object_or_404(Team, name=form.cleaned_data.get('team_name', None))
            for event_name in events:
                event = get_object_or_404(Event, name=event_name)
                event.participant_teams.add(team.pk)
                event.save()
            return HttpResponse('Registration successful. Congratulations!', content_type='text/plain')
    else:    
        form = EventRegistrationForm()
    
    template_data = {
        'form': form,
    }
    return render_to_response('registration/event_registration.html', template_data, context_instance=RequestContext(request))

def get_team(request):
    if request.method == "GET":
        team = get_object_or_404(Team, name=request.GET.get('team_name', None))
        participants = []
        for participant in team.participants.all():
            participants.append(participant.name)
        data = dumps(participants)
        return HttpResponse(data, content_type="application/json")
    else:
        return HttpResponseBadRequest()

def get_user(request):
    if request.method == "GET":
        user = get_object_or_404(UserProfile, username=request.GET.get('username', None))
        data = user.name
        return HttpResponse(data, content_type="text/plain")
    else:
        return HttpResponseBadRequest()

def serialize_to_json(request):
    try:
        eventname = request.POST.get('event_name', None)
        event = Event.objects.get(name=eventname)
        event_dict = {
                      'event_name': event.name, 
                      'intro': event.introduction , 
                      'probstat': event.problem_statement ,
                      'rules': event.rules_and_regulations,
                      'contacts': event.contacts
                     }
        data = dumps(event_dict)
        response = HttpResponse(data, content_type="application/json")
    except Event.DoesNotExist:
        raise Http404
    return HttpResponse(response)
    
@login_required
def my_page(request):
    #Selecting the event_notification queryset relating to the currently logged in user. 
    #(on the basis of the events he has registered for)
    user = UserProfile.objects.get(username = request.user)
    team_set = user.team_set.all()
    eventnotif_set = None
    for team in team_set:
        event_set = team.event_set.all()
        for event in event_set:
            eventnotif_set = event.eventnotification_set.all()
    
    # At this point if there are no event notifications for the 'user' then eventnotif_set is None
    eventnotif_list = []
    if eventnotif_set != None:
        eventnotif_set = eventnotif_set.distinct()

        #Converting  the eventnotif_set queryset object to a JSON response

        for i in range(0,len(eventnotif_set)):
            eventnotif_list +=[{ 
                                    'title' : eventnotif_set[i].title,
                                    'body': eventnotif_set[i].body
                                }]
    else:
        eventnotif_list = []

    eventnotif_dict = {'event_notifications' : eventnotif_list }
    data = dumps(eventnotif_dict)
    return HttpResponse(data, content_type="application/json")

def return_children(request):
    event = request.GET.get('event_name')
    children = []
    for child in Event.objects.all():
        if child.parent_event == event:
            children.append(child)
    data = dumps(children)
    return HttpResponse(data, content_type="application/json")