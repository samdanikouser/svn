from django.shortcuts import redirect, render

from apps.authentication.decorators import role_required
from apps.authentication.models import UserProfile
from apps.correctiveaction.models import CorrectiveAction
from apps.haccp.forms import CoolingDataForm
from apps.haccp.models import CookingData, CoolingData, HaccpAdminData, ReHeatingData
from apps.location.models import ControlPoint, Location
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from apps.usersapp.models import DailyUpdates
from django.contrib import messages
from datetime import timedelta



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
def daily_activity(request,location=None):
    location = Location.objects.get(name=location)
    name = location.name
    daily_activity = HaccpAdminData.objects.filter(storage_location =location)
    return render(request, 'users/users_first_page.html',{"location":name,"daily_activity":daily_activity})


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


def cooling_data_entry(request,location=None):
    corrective_actions=CorrectiveAction.objects.filter(control_point__name__istartswith='cool',control_point__location__name = location).values_list('name',flat=True)
    control_point = ControlPoint.objects.filter(location__name = location,name__istartswith='cool')
    if control_point:
        control_point = control_point[0]
    if request.method == 'POST':
        data = json.loads(request.body)
        location = Location.objects.get(name = data.get('storage_location'))
        sub_location = ControlPoint.objects.get(name =data.get('sub_storage_location'),location = location)
        cooling_data = CoolingData()
        cooling_data.storage_location = location
        cooling_data.sub_storage_location = sub_location
        cooling_data.food_item = data.get('food_item')
        cooling_data.internal_temp_at_0_hrs = data.get('temp_0')
        cooling_data.internal_temp_at_1_hrs =  data.get('temp_1')
        cooling_data.internal_temp_at_2_hrs = data.get('temp_2')
        cooling_data.internal_temp_at_3_hrs = data.get('temp_3')
        cooling_data.internal_temp_at_4_hrs = data.get('temp_4')
        cooling_data.internal_temp_at_5_hrs = data.get('temp_5')
        cooling_data.internal_temp_at_6_hrs = data.get('temp_6')
        cooling_data.cooling_methods = data.get('cooling_methods')
        cooling_data.data_entered_by = data.get('category')
        cooling_data.corrective_actions = data.get('corrective_actions')
        cooling_data.text_message = data.get('text_message')
        cooling_data.action_comment = data.get('action_comment')
        cooling_data.data_entered_by = UserProfile.objects.get(user = request.user)
        cooling_data.created_by = UserProfile.objects.get(user = request.user)
        cooling_data.save()
        return JsonResponse({"success": True})
    return render(request, 'users/cooling_data_entry.html',{"location":location,'control_point':control_point,'corrective_actions':list(corrective_actions)})


def cooling_data_list(request,location):
    coolings_data = CoolingData.objects.filter(storage_location__name = location)
    return render(request, 'users/cooling_data_list.html',{"location":location,'coolings_data':coolings_data})

def cooling_data_view(request,id):
    coolings_data = CoolingData.objects.filter(id = id)[0]
    return render(request, 'users/cooling_data_view.html',{'coolings_data':coolings_data})


def cooking_data_entry(request,location=None):
    corrective_actions=CorrectiveAction.objects.filter(control_point__name__istartswith='cool',control_point__location__name = location).values_list('name',flat=True)
    control_point = ControlPoint.objects.filter(location__name = location,name__istartswith='cool')
    if control_point:
        control_point = control_point[0]
    if request.method == 'POST':
        data = json.loads(request.body)
        location = Location.objects.get(name = data.get('storage_location'))
        sub_location = ControlPoint.objects.get(name =data.get('sub_storage_location'),location = location)
        cooking_data = CookingData()
        cooking_data.storage_location = location
        cooking_data.sub_storage_location = sub_location
        cooking_data.meal_period = data.get('meal_period')
        cooking_data.item_name = data.get('food_item')
        cooking_data.time = data.get('time')
        cooking_data.temperature = data.get('temperature')
        cooking_data.food_type = data.get('food_type')
        cooking_data.corrective_actions = data.get('corrective_actions')
        cooking_data.text_message = data.get('text_message')
        cooking_data.action_comment = data.get('action_comment')
        cooking_data.data_entered_by = UserProfile.objects.get(user = request.user)
        cooking_data.save()
        return JsonResponse({"success": True})
    return render(request, 'users/cooking_data_entry.html',{"location":location,'control_point':control_point,'corrective_actions':list(corrective_actions)})

def cooking_data_list(request,location):
    cookings_data = CookingData.objects.filter(storage_location__name = location)
    return render(request, 'users/cooking_data_list.html',{"location":location,'cookings_data':cookings_data})


def cooking_data_view(request,id):
    cookings_data = CookingData.objects.filter(id = id)[0]
    return render(request, 'users/cooking_data_view.html',{'cookings_data':cookings_data})


def reheating_data_entry(request,location=None):
    corrective_actions=CorrectiveAction.objects.filter(control_point__name__istartswith='cool',control_point__location__name = location).values_list('name',flat=True)
    control_point = ControlPoint.objects.filter(location__name = location,name__istartswith='cool')
    if control_point:
        control_point = control_point[0]
    if request.method == 'POST':
        data = json.loads(request.body)
        location = Location.objects.get(name = data.get('storage_location'))
        sub_location = ControlPoint.objects.get(name =data.get('sub_storage_location'),location = location)
        reheating_data = ReHeatingData()
        reheating_data.storage_location = location
        reheating_data.sub_storage_location = sub_location
        reheating_data.food_item =  data.get('food_item')
        reheating_data.date_of_reheating =  data.get('date_of_reheating')
        reheating_data.reheating_temperature =  data.get('temp')
        duration = timedelta(minutes= data.get('time_taken'))
        reheating_data.time_taken_for_reheating = duration
        reheating_data.action_comment =  data.get('action_comment')
        reheating_data.corrective_actions =  data.get('corrective_actions')
        reheating_data.data_entered_by = UserProfile.objects.get(user = request.user)
        reheating_data.save()
        return JsonResponse({"success": True})
    return render(request, 'users/reheating_data_entry.html',{"location":location,'control_point':control_point,'corrective_actions':list(corrective_actions)})


def reheating_data_list(request,location):
    reheating_data = ReHeatingData.objects.filter(storage_location__name = location)
    return render(request, 'users/reheating_data_list.html',{"location":location,'reheating_data':reheating_data})


def reheating_data_view(request,id):
    reheating_data = ReHeatingData.objects.filter(id = id)[0]
    return render(request, 'users/reheating_data_view.html',{'reheating_data':reheating_data})
