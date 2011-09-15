from django.contrib.auth.forms import UserCreationForm
from technex.app.models import UserProfile
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect

class RegistrationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'username', 'password1', 'password2', 'email', 'contact', 'gender', 'college',)

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    
    templateData = {
                    'form': form,
                    }
    return render_to_response('form.html', templateData, context_instance=RequestContext(request))

def serialize_to_json(request,eventname):
	try:
		e = str(eventname)
		e = Event.objects.filter(name=e)
		data = serializers.serialize("json", e)
		response = HttpResponse(data, mimetype="application/json")
	except ObjectDoesNotExist:
		response = "<html><body> <h1>" + eventname + "</h1> </body> </html>"
	return HttpResponse(response)
