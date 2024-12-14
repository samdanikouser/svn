from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.authentication.models import UserProfile
from apps.department.models import Department
from apps.personalhygiene.models import PersonalHygiene, UploadedPhoto
from ..authentication.decorators import role_required
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
import os
from weasyprint import HTML
from django.template.loader import render_to_string
from django.conf import settings
from calendar import month_name
import zipfile


@login_required
@role_required(allowed_roles=['admin', 'managers'])
def personalhygiene_list(request):
    if request.method == "GET":
        months = [(str(i), month_name[i]) for i in range(1, 13)]
        departments = Department.objects.filter(status=True)
        filter_type = request.GET.get('filter_type', '')
        inspected_date = request.GET.get('inspected_date', '')
        inspected_by = request.GET.get('inspected_by', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        month = request.GET.get('month', '')
        year = request.GET.get('year', '')
        department = request.GET.get('department', '')

        # Start with all records
        personal_hygiene_records = PersonalHygiene.objects.all()

        # Apply filters based on filter type
        if filter_type == "date" and inspected_date:
            personal_hygiene_records = personal_hygiene_records.filter(inspected_date=inspected_date)
        elif filter_type == "range" and start_date and end_date:
            personal_hygiene_records = personal_hygiene_records.filter(inspected_date__range=[start_date, end_date])
        elif filter_type == "monthly" and month:
            personal_hygiene_records = personal_hygiene_records.filter(inspected_date__month=month)
        elif filter_type == "yearly" and year:
            personal_hygiene_records = personal_hygiene_records.filter(inspected_date__year=year)
        elif filter_type == "department":
            personal_hygiene_records = personal_hygiene_records.filter(employee__department=department)
        elif inspected_by:
            personal_hygiene_records = personal_hygiene_records.filter(inspected_by__name__icontains=inspected_by)
        return render(request, 'personal_hygiene/list.html', {
            'records': personal_hygiene_records,
            'filter_type': filter_type,
            'inspected_date': inspected_date,
            'start_date': start_date,
            'end_date': end_date,
            'month': month,
            'year': year,
            'inspected_by': inspected_by,
            'department':departments,
            'months':months
        })


    return render(request, 'personal_hygiene/list.html',{'department':departments,'months':months})


@login_required
@role_required(allowed_roles=['admin','managers','supervisor'])
def add_personalhygiene(request):
    user_role = request.user.userprofile.role
    if user_role == "supervisor":
        user_profiles = UserProfile.objects.filter(role='line_staff')
    elif user_role == "managers":
       user_profiles = UserProfile.objects.filter(role='supervisor')
    else:
        user_profiles = UserProfile.objects.all()
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
        personal_hygiene.inspector_signature = request.POST['inspector_signature']
        personal_hygiene.employee_signature = request.POST['employee_signature']
        personal_hygiene.status = True
        personal_hygiene.save()
        photos_of = request.FILES.getlist('photos')
        for photos in photos_of:
            file_path = default_storage.save(f"media/personal_hygiene_photos/{photos.name}", photos)
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
def view_personalhygiene(request,id):
    inspection = PersonalHygiene.objects.get(pk=id)
    return render(request, 'personal_hygiene/view.html', {'personal_hygiene': inspection})


@login_required
@role_required(allowed_roles=['admin','managers'])
def download_filtered_pdf(request):
    # Get filter parameters
    filter_type = request.GET.get('filter_type', '')
    inspected_date = request.GET.get('inspected_date', '')
    inspected_by = request.GET.get('inspected_by', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    month = request.GET.get('month', '')
    year = request.GET.get('year', '')
    department = request.GET.get('department', '')
    
    if not isinstance(department, str):
        department = ''

    # Start building the query to filter the Personal Hygiene records
    personal_hygiene_records = PersonalHygiene.objects.all()
    
    if filter_type == "date" and inspected_date:
        personal_hygiene_records = personal_hygiene_records.filter(inspected_date=inspected_date)
    elif filter_type == "range" and start_date and end_date:
        personal_hygiene_records = personal_hygiene_records.filter(inspected_date__range=[start_date, end_date])
    elif filter_type == "monthly" and month:
        personal_hygiene_records = personal_hygiene_records.filter(inspected_date__month=month)
    elif filter_type == "yearly" and year:
        personal_hygiene_records = personal_hygiene_records.filter(inspected_date__year=year)
    elif filter_type == "department":
        personal_hygiene_records = personal_hygiene_records.filter(employee__department=department)
    elif inspected_by:
        personal_hygiene_records = personal_hygiene_records.filter(inspected_by__name__icontains=inspected_by)

    # Create a folder to store the PDFs if it doesn't exist
    pdf_folder = os.path.join(settings.BASE_DIR, 'personal_hygiene_pdfs')
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    # Iterate over each record, generate PDF, and save it
    for record in personal_hygiene_records:
        # Build absolute URLs for all photos associated with the record
        photo_urls = []
        for photo in record.photos.all():
            # Ensure the photo is accessible via absolute URL
            photo_url = request.build_absolute_uri(photo.photo.url)
            photo_urls.append(photo_url)

        # Render the HTML content for the current personal hygiene record
        html_content = render_to_string('personal_hygiene/download_format.html', {
            'personal_hygiene': record,
            'photo_urls': photo_urls  # Pass the list of photo URLs to the template
        })

        # Convert HTML to PDF using WeasyPrint
        pdf_file_path = os.path.join(pdf_folder, f"{record.employee.name}_{record.id}.pdf")
        HTML(string=html_content).write_pdf(pdf_file_path)

    # Create a zip file containing all the PDFs
    zip_filename = 'personal_hygiene_records.zip'
    zip_path = os.path.join(pdf_folder, zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for pdf_file in os.listdir(pdf_folder):
            if pdf_file.endswith('.pdf'):
                zipf.write(os.path.join(pdf_folder, pdf_file), pdf_file)

    # Provide the zip file for download
    with open(zip_path, 'rb') as zipf:
        response = HttpResponse(zipf.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={zip_filename}'
        return response
