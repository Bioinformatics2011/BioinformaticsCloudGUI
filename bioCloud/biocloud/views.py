# Create your views here.
from django.shortcuts import render_to_response
from biocloud.forms import UploadForm
from biocloud.models import UserFile
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
    return render_to_response('biocloud/index.html', context_instance=RequestContext(request))

def upload_popup(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = UserFile(userFile=request.FILES['userFile'])
            newdoc.userName = request.user.username
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('biocloud.views.upload_popup'))
    else:
        form = UploadForm() 
    # A empty, unbound form
    # Load documents for the list page
    files = UserFile.objects.filter(userName=request.user.username)
    # Render list page with the documents and the form
    return render_to_response(
        'biocloud/upload_popup.html',
        {'files': files, 'form': form},
        context_instance=RequestContext(request)
    )
