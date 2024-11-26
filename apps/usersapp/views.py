from django.shortcuts import render

from apps.haccp.models import HaccpAdminData
from apps.location.models import Location


# Create your views here.

def usersFirstDisplay(request):
    locations = Location.objects.filter(status=True)
    return render(request, 'users_first_page.html', {'locations': locations})

def userLogin(request,name):
    return render(request, 'login.html', {'name': name})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def check_range(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        entered_min = data['entered_min']
        entered_max = data['entered_max']

        item= HaccpAdminData.object.get(id=int(item_id))

        # Check if entered values are out of range
        if entered_min < item.min_temp or entered_max > item.max_temp:
            corrective_actions = ["Adjust settings", "Review limits"]  # Example actions
            return JsonResponse({"out_of_range": True, "corrective_actions": corrective_actions})

        return JsonResponse({"out_of_range": False})


@csrf_exempt
def save_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['item_id']
        min_value = data['min_value']
        max_value = data['max_value']
        corrective_actions = data.get('corrective_actions', [])

        # Save the data (logic here)
        # YourModel.objects.filter(id=item_id).update(min=min_value, max=max_value, corrective_actions=corrective_actions)

        return JsonResponse({"success": True})
