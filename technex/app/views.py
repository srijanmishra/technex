from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth import logout
from django.forms import ModelForm, CheckboxSelectMultiple
from django.forms.widgets import *
from technex.app.models import *
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from simplejson import dumps

class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'username', 'password1', 'password2', 'email', 'contact', 'gender', 'college',)

#class TeamRegistrationForm(ModelForm):
#    def __init__(self, user, *args, **kwargs):
#        team_set = user.team_set.all()
#        self.fields['participants'].queryset = team_set
#    class Meta:
#        model = Team
#        fields = ('name', 'participants',)
#        widgets = {
#                  'participants': SelectMultiple,
#                    }

class TeamRegistrationForm(ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'participants',)
        widgets = {
            'participants': CheckboxSelectMultiple,
        }

class EventRegistrationForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'participant_teams',)
        widgets = {
            'participant_teams': CheckboxSelectMultiple,
        }

#def logout_view(request):
    #logout(request)
    # Redirect to a success page.

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
    #Team Registration form generator & validator
    error = False
    reg_success = False
    if request.method == "POST":
        print request.POST
        form = TeamRegistrationForm(request.POST)
        if form.is_valid():
            #To check whether user has not entered more than 5 members, b4 saving in the database & commiting.          
            new_team = form.save(commit= False)
            #if len(new_team.participants) <= 5:
                #new_team.save()
                #form.save_m2m()
            reg_success = True
        else:
            error = True
    else:
        form = TeamRegistrationForm()
    template_data = {
        'form': form,
        'error': error,
        'registration_successful': reg_success
    }
    return render_to_response('registration/registration_team.html', template_data, context_instance=RequestContext(request))

def event_registration(request):
    #Event Registration form generator & validator
    error = False
    reg_success = False
    if request.method == "POST":
        form = EventRegistrationForm(request.POST)
        if form.is_valid():         
            form.save()
            reg_success = True
        else:
            error = True
    else:
        form = EventRegistrationForm()
    template_data = {
        'form': form,
        'error': error,
        'registration_successful': reg_success
    }
    return render_to_response('registration/registration_event.html', template_data, context_instance=RequestContext(request))

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
    user = UserProfile.objects.get(name = request.user)
    team_set = user.team_set.all()
    eventnotif_set = None
    for team in team_set:
        event_set = team.event_set.all()
        for event in event_set:
            eventnotif_set = event.eventnotification_set.all()
    
    # At this point if there are no event notifications for the 'user' then eventnotif_set is None
    eventnotif_list = []
    if eventnotif_set != None :
        eventnotif_set = eventnotif_set.distinct()

        #Converting  the eventnotif_set queryset object to a JSON response

        for i in range(0,len(eventnotif_set)):
            eventnotif_list +=[{ 
                                    'title' : eventnotif_set[i].title,
                                    'body': eventnotif_set[i].body
                                }]
    else:
        eventnotif_list +=[{ 
                                'title' : 'NOTIFICATIONS EMPTY ',
                                'body': 'HEY! YOU DO NOT HAVE ANY NOTIFICATIONS SPECIFIC TO THE EVENTS YOU HAVE REGISTERED FOR'
                           }]

    eventnotif_dict = {'event_notifications' : eventnotif_list }
    data = dumps(eventnotif_dict)
    return HttpResponse(data, content_type="application/json")
