from django.shortcuts import redirect, render

from apps.authentication.decorators import role_required
from apps.authentication.models import UserProfile
from apps.correctiveaction.models import CorrectiveAction
from apps.haccp.models import HaccpAdminData
from apps.location.models import Location
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from apps.usersapp.models import DailyUpdates
from django.contrib import messages


@login_required
@role_required(allowed_roles=['admin','managers','supervisor'])
def pending_approvals(request):
        user_role = request.user.userprofile.role
        if user_role == "supervisor":
            user_data = DailyUpdates.objects.filter(supervisor_approved_by__isnull=True)
        elif user_role == "admin" or user_role == "managers":
            user_data = DailyUpdates.objects.filter(manager_approved_by__isnull=True,supervisor_approved_by__isnull=False)        
        return render(request, 'pending_approvals/pending_approvals.html',{"user_data":user_data})


@login_required
@role_required(allowed_roles=['admin','managers','supervisor'])
def approve_tasks(request):
    user_data = DailyUpdates.objects.filter(supervisor_approved_by__isnull=True)

    if request.method == 'POST':
        selected_task_ids = request.POST.getlist('selected_tasks')  # List of selected task IDs
        supervisor = UserProfile.objects.get(user=request.user).name
        if selected_task_ids:
            tasks_to_approve = DailyUpdates.objects.filter(id__in=selected_task_ids)
            tasks_to_approve.update(supervisor_approved_status='approved',supervisor_approved_by=supervisor)
            messages.success(request, f'Approved successful!')
            return render(request, 'pending_approvals/pending_approvals.html',{"user_data":user_data})
        return render(request, 'pending_approvals/pending_approvals.html',{"user_data":user_data})



@login_required
def daily_activity(request):
    location = Location.objects.get(id=request.GET.get('location')).name
    daily_activity = HaccpAdminData.objects.filter(storage_location = Location.objects.get(id=request.GET.get('location')))
    return render(request, 'users/users_first_page.html',{"location":location,"daily_activity":daily_activity})


@csrf_exempt
def check_range(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        entered_temp = float(data['temperature_value'])
        item= HaccpAdminData.objects.get(id=int(item_id))

        # Check if entered values are out of range
        if entered_temp < item.min_temp or entered_temp > item.max_temp:
            corrective_actions = list(item.corrective_action.filter(status=True).values('id','name'))
            return JsonResponse({"out_of_range": True, "corrective_actions": corrective_actions})

        return JsonResponse({"out_of_range": False})


@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_data = DailyUpdates()
        user_data.haccp_link = HaccpAdminData.objects.get(id=int(data['item_id']))
        user_data.temperature_value = data['temperature_value']
        user_data.haccp_link_time_given = data['time']
        if 'corrective_actions' in data:
            for actions in data.get('corrective_actions', []):
                corrective_action_name = CorrectiveAction.objects.get(id=int(actions)).name
                if user_data.corrective_actions:
                    user_data.corrective_actions += f", {corrective_action_name}"
                else:
                    user_data.corrective_actions = corrective_action_name
            user_data.text_message = data['comment']
        user_data.created_by = UserProfile.objects.get(user = request.user)
        user_data.save()

        return JsonResponse({"success": True})


def check_daily_update(request):
    user_data = DailyUpdates.objects.filter().values_list('haccp_link_time_given','haccp_link__used_for')
    data_to_send = [{'id':data[1]+str(data[0])[0:5]} for data in user_data]
    return JsonResponse({'data_exists': data_to_send})