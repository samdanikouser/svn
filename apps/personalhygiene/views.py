from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.authentication.models import UserProfile
from apps.personalhygiene.forms import PersonalHygieneForm
from apps.personalhygiene.models import PersonalHygiene
from ..authentication.decorators import role_required
from django.contrib import messages


@login_required
@role_required(allowed_roles=['admin','managers'])
def personalhygiene_list(request):
    pass

@login_required
@role_required(allowed_roles=['admin','managers','supervisor'])
def add_personalhygiene(request):
    user_role = request.user.userprofile.role
    if user_role == "supervisor":
        user_profiles = UserProfile.objects.filter(role='line_staff')
    elif user_role == "managers":
       user_profiles = UserProfile.objects.filter(role='supervisor')
    else:
        user_profiles = UserProfile.objects.filter()
    if request.method == "POST":
        knowledge_of_personal_hygiene = request.POST.get('knowledge_of_personal_hygiene')
        trimmed_beard_moustache = request.POST.get('trimmed_beard_moustache')
        overall_health = request.POST.get('overall_health')
        short_nails = request.POST.get('short_nails')
        overall_cleanliness = request.POST.get('overall_cleanliness')
        cleaned_hands = request.POST.get('cleaned_hands')
        proper_uniform = request.POST.get('proper_uniform')
        trimmed_hair = request.POST.get('trimmed_hair')
        print(knowledge_of_personal_hygiene)
        personal_hygiene = PersonalHygiene()
        personal_hygiene.employee = UserProfile.objects.get(id=int(request.POST['employee']))
        personal_hygiene.inspected_date = request.POST['inspection_date']
        personal_hygiene.inspected_by = UserProfile.objects.get(user=request.user)
        personal_hygiene.parameters_checked = trimmed_hair
        personal_hygiene.status = True
        personal_hygiene.photos = request.FILES
        personal_hygiene.save()
        messages.success(request, 'Added successfully!')
        return redirect('personalhygiene/add/')
    return render(request, "personal_hygiene/add.html",{'user_profiles': user_profiles})


@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_personalhygiene(request,id):
    pass

@login_required
@role_required(allowed_roles=['admin','managers'])
def update_personalhygiene(request,id):
    pass