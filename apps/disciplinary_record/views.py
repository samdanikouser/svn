from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from apps.authentication.decorators import role_required
from django.contrib import messages
import json
from apps.authentication.models import UserProfile
from apps.disciplinary_record.models import DisciplinaryRecord


@login_required
@role_required(allowed_roles=['admin','managers','supervisor'])
def add_disciplinary_record(request):
    user_role = request.user.userprofile.role
    if user_role == "supervisor":
        user_profiles = UserProfile.objects.filter(role='line_staff')
    elif user_role == "managers":
       user_profiles = UserProfile.objects.filter(role='supervisor')
    else:
        user_profiles = UserProfile.objects.all()
    employee_records = {
        profile.id: DisciplinaryRecord.objects.filter(employee=profile).exists()
        for profile in user_profiles
    }
    if request.method == "POST":
        record = DisciplinaryRecord()
        record.employee =UserProfile.objects.get(employee_id =int(request.POST['employee_id']))
        record.issues_realted_to = request.POST['category']
        record.incident_date = request.POST['incident_date']
        record.reason = request.POST['description']
        record.inspector_signature = request.POST['inspector_signature']
        record.employee_signature = request.POST['employee_signature']
        record.recorded_by = UserProfile.objects.get(user=request.user)
        record.save()
        messages.success(request, 'Recorded successfully!')
        return redirect('/disciplinary_record/add')
    return render(request, "disciplinary_record/add.html",{'user_profiles': user_profiles,'employee_records': json.dumps(employee_records)})


@login_required
@role_required(allowed_roles=['admin','managers','supervisor'])
def list_disciplinary_record(request,id):
    records = DisciplinaryRecord.objects.filter(employee__id=int(id))
    return render(request, "disciplinary_record/list.html",{'records':records})



@login_required
@role_required(allowed_roles=['admin','managers','supervisor'])
def view_disciplinary_record(request,id):
    records = DisciplinaryRecord.objects.get(id=int(id))
    return render(request, "disciplinary_record/view.html",{'records':records})
