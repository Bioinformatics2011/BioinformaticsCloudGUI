# Create your views here.
from django.shortcuts import render_to_response
from biocloud.models import *
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect,\
    HttpResponseBadRequest, Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.middleware.csrf import get_token
from django.utils import simplejson
import os
import re
import json
import stat 
from django.views.decorators.csrf import csrf_exempt  
from io import BufferedWriter, FileIO

def index(request):
    return render_to_response('biocloud/index.html', context_instance=RequestContext(request))

def workflow(request):
    if request.method == 'POST': # If the form has been submitted...
        # Because django supports static, backend-generated forms,
        # but we generate our in the browser
        # we try a non-pythonic solution, using DotExpandedDict
        from django.utils.datastructures import DotExpandedDict
        # do some escaping at this point?
        data = DotExpandedDict(request.POST)
        
        request.session['projectName'] = request.POST['projectName']
        aProject = project.Project(request.session['projectName'], settings.PROJECT_FOLDER + request.session['projectName'])
        
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
            .join([program.commandLineScript(aProject)
                        for program in workflow]))
    else:
        projectName = request.session.get('projectName', '')
        files = []
        if not projectName == '':
            files = os.listdir(settings.PROJECT_FOLDER + projectName)
        
        file_info_list = []
        for file_name in files:
            file_info = {
                'fname': file_name,
                'fsize': os.stat(settings.PROJECT_FOLDER + projectName + "/" + file_name) [stat.ST_SIZE],
            }
            if not os.path.isdir(settings.PROJECT_FOLDER + projectName + "/" + file_name):
                file_info_list.append(file_info)
            
        ctx = RequestContext(request, {
            'csrf_token': get_token(request),
        })
        return render_to_response('biocloud/workflow.html',
            {'programs': [__importClass__(program).asJson() for program in settings.APPLICATIONS],
             'projects': filter(lambda each: os.path.isdir(settings.PROJECT_FOLDER + each),
                                os.listdir(settings.PROJECT_FOLDER)),
             'selectedProject': projectName,
             'files': file_info_list},
            context_instance=ctx)
        
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

@csrf_exempt # this is not good, but without it i get error 403, even if i send csrf_token.. 
def xhr_upload(request):
    if request.method == "POST":
        if request.is_ajax():
            upload = request
            is_raw = True
            try:
                filename = request.GET['qqfile']
            except KeyError:
                return HttpResponseBadRequest("Ajax request not valid")
        else:
            is_raw = False
            if len(request.FILES) == 1:
                upload = request.FILES.values()[0]
            else:
                raise Http404("Bad Upload")
            filename = upload.name
        success = save_upload(upload, filename, is_raw,request.GET['current_project'])
        ret_json = {'success':success,}
        return HttpResponse(json.dumps(ret_json))

def save_upload( uploaded, filename, raw_data, directory ):
    '''
      raw_data: if True, uploaded is an HttpRequest object with the file being
            the raw post data
            if False, uploaded has been submitted via the basic form
            submission and is a regular Django UploadedFile in request.FILES
    '''
    try:
        with BufferedWriter( FileIO(settings.PROJECT_FOLDER+directory+"/"+filename, "wb")) as dest:
            if raw_data:
                foo = uploaded.read(1024)
                while foo:
                    dest.write(foo)
                    foo = uploaded.read(1024)
            else:
                for c in uploaded.chunks():
                    dest.write(c)
            return True
    except IOError:
        pass
    return False

def xhr_folderContents(request, projectName):
    path = settings.PROJECT_FOLDER + projectName
    if os.path.exists(path) and os.path.isdir(path):
        files = os.listdir(path)
        file_info_map = {}
        for file_name in files:
            file_info = {
                'fname': file_name,
                'fsize': os.stat(path +"/" + file_name) [stat.ST_SIZE],
            }
            if not os.path.isdir(path +"/" + file_name):
                file_info_map[file_name] = file_info
        return HttpResponse(simplejson.dumps(file_info_map))
    else:
        return HttpResponse("Project does not exist.")
       
def __importClass__(someString):
    (module, className) = someString.rsplit('.', 1)
    Module = __import__(module, globals(), locals(), [className])
    return getattr(Module, className)
    
