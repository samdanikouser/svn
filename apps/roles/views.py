from django.shortcuts import render, redirect, HttpResponse
from .models import Roles
from .forms import RoleForm


# Create your views here.

def location_roles(request):
    roles = Roles.objects.all()
    return render(request, "roles/list.html", {'roles': roles})


# add employee function
def add_roles(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.save()
            return redirect("/roles/list")
        else:
            return render(request, "add.html",
                          {"form": form})
    return render(request, "add.html", {"form": RoleForm()})


# employee delete function
def delete_roles(request, id):
    # listings/views.py
    roles = Roles.objects.get(pk=id)
    if request.method == "POST":
        roles.delete()
        return redirect("/role/list")
    return render(request,
                  'delete.html',
                  {'roles': roles})


# update employee
def update_roles(request, id):
    roles = Roles.objects.get(pk=id)
    if request.method == "POST":
        form = RoleForm(request.POST, instance=roles)
        if form.is_valid():
            form.save()
            return redirect("/roles/list")
        else:
            return render(request, "update.html",
                          {"roles": roles, "form": form})
    return render(request, "update.html", {"roles": roles, "form": RoleForm(instance=roles)})