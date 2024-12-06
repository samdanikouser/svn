from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Department
from .forms import DepartmentForm
from ..authentication.decorators import role_required
from django.contrib import messages


@login_required
@role_required(allowed_roles=['admin','managers'])
def department_list(request):
    department = Department.objects.all()
    return render(request, "department/list.html", {'department': department})


@login_required
@role_required(allowed_roles=['admin','managers'])
def add_department(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.save()
            messages.success(request, 'Department Added successfully!')
            print("samdani")
            return redirect("/department/list/")
    return render(request, "department/add.html", {"form": DepartmentForm()})


@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_department(request, id):
    department = Department.objects.get(pk=id)
    if request.method == "POST":
        print("samdani deke")
        department.delete()
        messages.success(request, 'Department Deleted successfully!')
        return redirect("department/list")
    return render(request,
                  'department/delete.html',
                  {'department': department})


@login_required
@role_required(allowed_roles=['admin','managers'])
def update_department(request, id):
    department = Department.objects.get(pk=id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department Updated successfully!')
            return redirect("/department/list")
        else:
            return render(request, "department/update.html",
                          {"department": department, "form": form})
    return render(request, "department/update.html", {"department": department, "form": DepartmentForm(instance=department)})