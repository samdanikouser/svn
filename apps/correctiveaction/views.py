from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import CorrectiveAction
from .forms import ActionForm
from apps.location.models import Location
from ..authentication.decorators import role_required


@login_required
@role_required(allowed_roles=['admin','managers'])
def action_list(request):
    locations = Location.objects.all()
    action = CorrectiveAction.objects.all()
    return render(request, "action/list.html", {'action': action,"locations":locations})


# add employee function
@login_required
@role_required(allowed_roles=['admin','managers'])
def add_action(request):
    locations = Location.objects.all()
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.save()
            return redirect("/action/list")
        else:
            return render(request, "action/add.html",
                          {"form": form,"locations":locations})
    return render(request, "action/add.html", {"form": ActionForm(),"locations":locations})


# employee delete function
@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_action(request, id):
    locations = Location.objects.all()
    action = CorrectiveAction.objects.get(pk=id)
    if request.method == "POST":
        action.delete()
        return redirect("/action/list")
    return render(request,
                  'action/delete.html',
                  {'action': action,"locations":locations})


# update employee
@login_required
@role_required(allowed_roles=['admin','managers'])
def update_action(request, id):
    locations = Location.objects.all()
    action = CorrectiveAction.objects.get(pk=id)
    if request.method == "POST":
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            return redirect("/action/list")
        else:
            return render(request, "action/update.html",
                          {"action": action, "form": form,"locations":locations})
    return render(request, "action/update.html", {"action": action, "form": ActionForm(instance=action),"locations":locations})