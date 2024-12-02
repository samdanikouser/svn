from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Location
from .forms import LocationForm
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
            messages.success(request, 'Location Added successfully!')
            return redirect("/location/list")
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