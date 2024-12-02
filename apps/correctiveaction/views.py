from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import CorrectiveAction
from .forms import ActionForm
from ..authentication.decorators import role_required
from django.contrib import messages


@login_required
@role_required(allowed_roles=['admin','managers'])
def action_list(request):
    action = CorrectiveAction.objects.all()
    return render(request, "action/list.html", {'action': action})


# add employee function
@login_required
@role_required(allowed_roles=['admin','managers'])
def add_action(request):
    if request.method == "POST":
        form = ActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.save()
            messages.success(request, 'Action Added successfully!')
            return redirect("/action/list")
        else:
            return render(request, "action/add.html",
                          {"form": form})
    return render(request, "action/add.html", {"form": ActionForm(),"locations":locations})


# employee delete function
@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_action(request, id):
    action = CorrectiveAction.objects.get(pk=id)
    if request.method == "POST":
        action.delete()
        messages.success(request, 'Action Deleted successfully!')
        return redirect("/action/list")
    return render(request,
                  'action/delete.html',
                  {'action': action})


# update employee
@login_required
@role_required(allowed_roles=['admin','managers'])
def update_action(request, id):
    action = CorrectiveAction.objects.get(pk=id)
    if request.method == "POST":
        form = ActionForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            messages.success(request, 'Action Updated successfully!')
            return redirect("/action/list")
        else:
            return render(request, "action/update.html",
                          {"action": action, "form": form})
    return render(request, "action/update.html", {"action": action, "form": ActionForm(instance=action)})