# Create your views here.
from django.shortcuts import render_to_response
from biocloud.forms import UploadForm
from biocloud.models import *
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
import os
import re

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

def workflow(request):
    if request.method == 'POST': # If the form has been submitted...
        # Because django supports static, backend-generated forms,
        # but we generate our in the browser
        # we try a non-pythonic solution, using DotExpandedDict
        from django.utils.datastructures import DotExpandedDict
        # do some escaping at this point?
        data = DotExpandedDict(request.POST)
        
        request.session['projectName'] = request.POST['projectName']
        
        candidates = [__importClass__(program) for program in settings.APPLICATIONS]
        workflow = []
        for i, program in data['program'].iteritems():
            stepNumber = int(i)
            for candidate in candidates:
                if program['programName'] == candidate.name():
                    workflow.insert(stepNumber, candidate(program, workflow, stepNumber))
                    break
        
        # now we have a list of Program instances ready to run
        return HttpResponse("<br />"
            .join([program.commandLineScript()
                        for program in workflow]))
    else:
        projectName = request.session.get('projectName', '')
        files = []
        if not projectName == '':
            files = os.listdir(settings.PROJECT_FOLDER + projectName)
        return render_to_response('biocloud/workflow.html',
            {'programs': [__importClass__(program).asJson() for program in settings.APPLICATIONS],
             'projects': filter(lambda each: os.path.isdir(settings.PROJECT_FOLDER + each),
                                os.listdir(settings.PROJECT_FOLDER)),
             'selectedProject': projectName,
             'files': files},
            context_instance=RequestContext(request))
        
def xhr_createProjectFolder(request):
    if request.is_ajax() and request.method == 'POST':
        projectName = request.POST['projectName']
        if (re.match("^[^/|\r\n]+$", projectName) and
                not os.path.exists(settings.PROJECT_FOLDER + projectName)):
            os.makedirs(settings.PROJECT_FOLDER + projectName)
            return HttpResponse(projectName)
        else:
            return HttpResponse("Project name is not a valid folder name, or the project already exists.")
    else:
        HttpResponseRedirect(reverse('biocloud.views.workflow'))

def xhr_folderContents(request, projectName):
    path = settings.PROJECT_FOLDER + projectName
    if os.path.exists(path) and os.path.isdir(path):
        files = os.listdir(path)
        return HttpResponse('["%s"]' % '", "'.join(files))
    else:
        return HttpResponse("Project does not exist.")
        
def __importClass__(someString):
    (module, className) = someString.rsplit('.', 1)
    Module = __import__(module, globals(), locals(), [className])
    return getattr(Module, className)
    