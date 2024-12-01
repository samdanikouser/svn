from django.shortcuts import render

from apps.haccp.models import HaccpAdminData
from apps.location.models import Location
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json


# Create your views here.

def usersFirstDisplay(request):
    locations = Location.objects.filter(status=True)
    return render(request, 'users/users_first_page.html', {'locations': locations})

def userLogin(request,name):
    return render(request, 'login.html', {'name': name})


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
        entered_min = float(data['entered_min'])
        entered_max = float(data['entered_max'])
        item= HaccpAdminData.objects.get(id=int(item_id))

        # Check if entered values are out of range
        if entered_min < item.min_temp or entered_max > item.max_temp:
            corrective_actions = list(item.corrective_action.filter(status=True).values('id','name'))
            return JsonResponse({"out_of_range": True, "corrective_actions": corrective_actions})

        return JsonResponse({"out_of_range": False})


@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        min_value = data['entered_min']
        max_value = data['entered_max']
        corrective_actions = data.get('corrective_actions', [])
        user_text = data['comment']

        # Save the data (logic here)
        # YourModel.objects.filter(id=item_id).update(min=min_value, max=max_value, corrective_actions=corrective_actions)

        return JsonResponse({"success": True})
