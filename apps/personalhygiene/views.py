from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.authentication.models import UserProfile
from apps.personalhygiene.forms import PersonalHygieneForm
from apps.personalhygiene.models import PersonalHygiene, UploadedPhoto
from ..authentication.decorators import role_required
from django.contrib import messages
from django.core.files.storage import default_storage


@login_required
@role_required(allowed_roles=['admin', 'managers'])
def personalhygiene_list(request):
    if request.method == "POST":
        inspected_date = request.GET.get('inspected_date', '')
        inspected_by = request.GET.get('inspected_by', '')
        personal_hygiene_records = PersonalHygiene.objects.all()
        if inspected_date:
            personal_hygiene_records = personal_hygiene_records.filter(inspected_date=inspected_date)
        if inspected_by:
            personal_hygiene_records = personal_hygiene_records.filter(inspected_by__icontains=inspected_by)
        return render(request, 'personal_hygiene/list.html', {
            'records': personal_hygiene_records,
            'inspected_date': inspected_date,
            'inspected_by': inspected_by,
        })
    return render(request, 'personal_hygiene/list.html',)

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
        parameters_checked = f"""{knowledge_of_personal_hygiene}
        {trimmed_beard_moustache}
        {overall_health}
        {short_nails}
        {overall_cleanliness}
        {cleaned_hands}
        {proper_uniform}
        {trimmed_hair}"""
        personal_hygiene = PersonalHygiene()
        personal_hygiene.employee = UserProfile.objects.get(id=int(request.POST['employee']))
        personal_hygiene.inspected_date = request.POST['inspection_date']
        personal_hygiene.inspected_by = UserProfile.objects.get(user=request.user)
        personal_hygiene.parameters_checked = parameters_checked
        personal_hygiene.status = True
        personal_hygiene.save()
        photos_of = request.FILES.getlist('photos')
        for photos in photos_of:
            file_path = default_storage.save(f"personal_hygiene_photos/{photos.name}", photos)
            UploadedPhoto.objects.create(photo=file_path)
            personal_hygiene.photos.add(UploadedPhoto.objects.create(photo=file_path))
        messages.success(request, 'Added successfully!')
        return redirect('/personalhygiene/add')
    return render(request, "personal_hygiene/add.html",{'user_profiles': user_profiles})


@login_required
@role_required(allowed_roles=['admin','managers'])
def delete_personalhygiene(request,id):
    pass

@login_required
@role_required(allowed_roles=['admin','managers'])
def update_personalhygiene(request,id):
    pass