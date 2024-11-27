from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.authentication.decorators import role_required
from apps.correctiveaction.models import CorrectiveAction
from apps.location.models import Location
from apps.roles.models import Roles
from apps.haccp.models import HaccpAdminData
from django.template import loader
from django.contrib import messages



@login_required
@role_required(allowed_roles=['admin','managers'])
def HaccpList(request):
    locations = Location.objects.all()
    HaccpList = HaccpAdminData.objects.all()
    return render(request,'haccp/list.html',{'hccp_list':HaccpList,"locations":locations})


@login_required
@role_required(allowed_roles=['admin','managers'])
def HaccpDelete(request,id):
    locations = Location.objects.all()
    HaccpList = HaccpAdminData.objects.get(pk=id)
    if request.method == "POST":
        HaccpList.delete()
        messages.success(request, 'Haccp deleted successful!')
        return redirect("/haccp/list")
    return render(request,'haccp/delete.html',{"locations":locations,'haccp':HaccpList})


@login_required
@role_required(allowed_roles=['admin','managers'])
def haccpHome(request, name):
    locations = Location.objects.all()
    context = {"name": name, "locations": locations}
    html_template = loader.get_template('haccp/haccphome.html')
    return HttpResponse(html_template.render(context, request))

@login_required
@role_required(allowed_roles=['admin','managers'])
def storagelocation(request, name, status):
    corrective_action = CorrectiveAction.objects.filter(status=True)
    locations = Location.objects.filter(status=True)
    roles = Roles.objects.all()
    return render(request, 'storageName/storageData.html',
                  {"roles": roles, "name": name, "status": status, "locations": locations,
                   "corrective_action": corrective_action})


@login_required
@role_required(allowed_roles=['admin','managers'])
def storagelocationAdminData(request, name, status):
    if request.method == "POST":
        storage_location = name
        sub_storage_location = status
        task_name = request.POST.get("taskName")
        used_for = request.POST.get("used_for")
        no_of_used_for = int(request.POST.get("no_of_used_for"))
        assign_task_to = request.POST.get("assign_task_to")
        repeat_every = request.POST.get("period")
        repeat_frequency = request.POST.get("repeat_frequency")
        time_on = request.POST.getlist("time_on")
        min_temp = request.POST.get("max_value")
        max_temp = request.POST.get("max_value")
        corrective_action = request.POST.getlist("corrective_action")
        assign_verifier = request.POST.get("select_verifier")
        for num_of_sub_storage in range(1,no_of_used_for+1):
            admin_data = HaccpAdminData()
            admin_data.storage_location = Location.objects.get(name = storage_location)
            admin_data.sub_storage_location =sub_storage_location
            admin_data.name =task_name
            admin_data.used_for =used_for+str(num_of_sub_storage)
            admin_data.assign_task_to =assign_task_to
            admin_data.repeat_every =repeat_every
            admin_data.repeat_frequency =repeat_frequency
            admin_data.assign_verifiers =assign_verifier
            admin_data.time_on =time_on
            admin_data.min_temp =min_temp
            admin_data.max_temp =max_temp
            admin_data.save()
            corrective_actions = CorrectiveAction.objects.filter(id__in=corrective_action)
            admin_data.corrective_action.set(corrective_actions)
    locations = Location.objects.all()
    messages.success(request, f'{sub_storage_location} task stored successful!')
    return render(request, 'haccp/list.html', {"locations": locations, "status": status, "name": name})
