from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.authentication.decorators import role_required

# Create your views here.

@login_required
@role_required(allowed_roles=['admin','managers'])
def stewarding(request):
    return render(request,'home/page-blank.html')
