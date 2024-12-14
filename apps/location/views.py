from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.correctiveaction.forms import ActionForm
from apps.correctiveaction.models import CorrectiveAction

from .models import ControlPoint, Location
from .forms import ControlPointForm, LocationForm
from ..authentication.decorators import role_required
from django.contrib import messages



@login_required
@role_required(allowed_roles=['admin','managers'])
def location_list(request):
    location = Location.objects.all()
    return render(request, "location/list.html", {'locations': location})


@login_required
@role_required(allowed_roles=['admin','managers'])
def add_location(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.save()
            print(location)
            messages.success(request, 'Location Added successfully,Add the control point and actions!')
            return redirect(f"{location}/control_point/add")
        else:
            return render(request, "location/add.html",
                          {"form": form})
    return render(request, "location/add.html", {"form": LocationForm()})


@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_location(request, id):
    location = Location.objects.get(pk=id)
    if request.method == "POST":
        location.delete()
        messages.success(request, 'Location Deleted successfully!')
        return redirect("/location/list")
    return render(request,
                  'location/delete.html',
                  {'location': location})


@login_required
@role_required(allowed_roles=['admin','managers'])
def update_location(request, id):
    location = Location.objects.get(pk=id)
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location Updated successfully!')
            return redirect("/location/list")
        else:
            return render(request, "location/update.html",
                          {"location": location, "form": form})
    return render(request, "location/update.html", {"location": location, "form": LocationForm(instance=location)})


@login_required
@role_required(allowed_roles=['admin','managers'])
def add_control_point(request,name):
    corrective_action_form = ActionForm()
    location = Location.objects.get(name=name)
    control_point_form = ControlPointForm(initial={'location': Location.objects.get(name=name)})
    if request.method == "POST":
        control_point_form = ControlPointForm(request.POST)
        corrective_action_data = request.POST.getlist('corrective_actions[][name]')
        corrective_action_status = request.POST.getlist('corrective_actions[][status]')

        if control_point_form.is_valid():
            control_point = control_point_form.save(commit=False)
            control_point.location = location  # Ensure location is set
            control_point.save()

            for action, status in zip(corrective_action_data, corrective_action_status):
                corrective_action = CorrectiveAction(
                    name=action,
                    status=status == 'True',
                    control_point=control_point,
                    created_by = request.user
                )
                corrective_action.save()

            messages.success(request, 'Control point Added successfully,add more if required!')
            return redirect(f"/location/{name}/control_point/add")
        else:
            return render(request, "location/add.html",
                          { "control_point_form": control_point_form,
        "corrective_action_form": corrective_action_form,})
    return render(request, "location/control_point_and_Action_Add.html",{ "control_point_form": control_point_form,
        "corrective_action_form": corrective_action_form,"location_name":name})


@login_required
@role_required(allowed_roles=['admin','managers'])
def list_control_point(request,id):
    location = Location.objects.get(id=id)
    control_point = ControlPoint.objects.filter(location = location)
    return render(request, "location/control_point_list.html", {'control_points': control_point,'location':location})


@login_required
@role_required(allowed_roles=['admin','managers'])
def update_control_point(request, id):
    controlPoint = ControlPoint.objects.get(pk=id)
    if request.method == "POST":
        form = ControlPointForm(request.POST, instance=controlPoint)
        if form.is_valid():
            form.save()
            messages.success(request, 'ControlPoint Updated successfully!')
            return redirect("/location/control-point/list/"+str(controlPoint.location.id))
        else:
            return render(request, "location/control_point_update.html",
                          {"controlPoint": controlPoint, "form": form})
    return render(request, "location/control_point_update.html", {"controlPoint": controlPoint, "form": ControlPointForm(instance=controlPoint)})


@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_control_point(request, id):
    controlPoint = ControlPoint.objects.get(pk=id)
    if request.method == "POST":
        controlPoint.delete()
        messages.success(request, 'Control Point Deleted successfully!')
        return redirect("/location/control-point/delete/"+str(controlPoint.location.id))
    return render(request,
                  'location/control_point_delete.html',
                  {'controlPoint': controlPoint})


@login_required
@role_required(allowed_roles=['admin','managers'])
def list_corrective_actions(request,id):
    control_point = ControlPoint.objects.get(id=id)
    actions = CorrectiveAction.objects.filter(control_point = control_point)
    return render(request, "action/list.html", {'actions': actions,'control_point':control_point})

@login_required
@role_required(allowed_roles=['admin','managers'])
def add_corrective_actions(request,id):
    control_point = ControlPoint.objects.get(id=id)
    if request.method == "POST":
        corrective_action_data = request.POST.getlist('corrective_actions[][name]')
        corrective_action_status = request.POST.getlist('corrective_actions[][status]')
        for action, status in zip(corrective_action_data, corrective_action_status):
                corrective_action = CorrectiveAction(
                    name=action,
                    status=status == 'True',
                    control_point=control_point,
                    created_by = request.user
                )
                corrective_action.save()
        messages.success(request, 'Control point Added successfully,add more if required!')
        return redirect(f"/location/corrective_actions/add/{id}")
    return render(request, "action/add.html",{'control_point':control_point})


@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_corrective_actions(request, id):
    correctiveAction = CorrectiveAction.objects.get(pk=id)
    if request.method == "POST":
        correctiveAction.delete()
        messages.success(request, 'Control Point Deleted successfully!')
        return redirect("/location/corrective_actions/list/"+str(correctiveAction.control_point.id))
    return render(request,
                  'action/delete.html',
                  {'correctiveAction': correctiveAction})

@login_required
@role_required(allowed_roles=['admin','managers'])
def update_corrective_actions(request, id):
    correctiveAction = CorrectiveAction.objects.get(id=id)
    form = ActionForm(instance=correctiveAction)
    if request.method == "POST":
        form = ActionForm(request.POST, instance=correctiveAction)
        if form.is_valid():
            form.save()
            messages.success(request, ' Corrective action Updated successfully!')
            return redirect("/location/corrective_actions/list/"+str(correctiveAction.id))
        else:
            return render(request, "action/update.html",
                          {"correctiveAction": correctiveAction, "form": form})
    return render(request, "action/update.html", {"correctiveAction": correctiveAction,'form':form})


