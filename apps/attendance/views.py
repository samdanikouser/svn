import face_recognition
import cv2
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Employee, Attendance
from datetime import datetime

def recognize_face(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        # Convert image to a format that face_recognition can process
        image = face_recognition.load_image_file(uploaded_image)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            face_encoding = encodings[0]
            employee = Employee.objects.filter(facial_encoding=face_encoding).first()

            if employee:
                # Check if attendance is already marked for today
                today = datetime.today().date()
                attendance = Attendance.objects.filter(employee=employee, time_in__date=today).first()

                if attendance:
                    # Mark time-out
                    attendance.time_out = datetime.now()
                    attendance.save()
                    return JsonResponse({'status': 'time-out'})
                else:
                    # Mark time-in
                    Attendance.objects.create(employee=employee, time_in=datetime.now())
                    return JsonResponse({'status': 'time-in'})
            else:
                return JsonResponse({'status': 'unknown face'})
        else:
            return JsonResponse({'status': 'no face detected'})
    return render(request, "attendance/recognize.html")

