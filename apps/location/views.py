from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from .models import Location
from .forms import LocationForm
from ..authentication.decorators import role_required
from django.contrib import messages



# Create your views here.
@login_required
@role_required(allowed_roles=['admin','managers'])
def location_list(request):
    location = Location.objects.all()
    return render(request, "location/list.html", {'locations': location})


# add employee function
@login_required
@role_required(allowed_roles=['admin','managers'])
def add_location(request):
    location = Location.objects.all()
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.save()
            messages.success(request, 'Location Added successfully!')
            return redirect("/location/list")
        else:
            return render(request, "location/add.html",
                          {"form": form,'locations': location})
    return render(request, "location/add.html", {"form": LocationForm(),'locations': location})


# employee delete function
@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_location(request, id):
    # listings/views.py
    locations = Location.objects.all()
    location = Location.objects.get(pk=id)
    if request.method == "POST":
        location.delete()
        messages.success(request, 'Location Deleted successfully!')
        return redirect("/location/list")
    return render(request,
                  'location/delete.html',
                  {'location': location,'locations':locations})


# update employee
@login_required
@role_required(allowed_roles=['admin','managers'])
def update_location(request, id):
    locations = Location.objects.all()
    location = Location.objects.get(pk=id)
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Location Updated successfully!')
            return redirect("/location/list")
        else:
            return render(request, "location/update.html",
                          {"location": location, "form": form,'locations':locations})
    return render(request, "location/update.html", {"location": location, "form": LocationForm(instance=location),'locations':locations})