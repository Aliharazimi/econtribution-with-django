from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from users.models import Contribution, Contributor, ContactUs
from django.template.loader import get_template
from django.conf import settings
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib import messages

def index(request):
    customercount=get_user_model().objects.all()
    contribution=Contribution.objects.all()
    contributors=Contributor.objects.all()

    context = {
        'customercount': customercount,
        'contribution': contribution,
        'contributors': contributors,
    }

    return render(request, 'core/index.html', context)

def about(request):
    return render(request, 'core/about.html')

def blog(request):
    return render(request, 'core/blog.html')


def contact_us(request):
    if request.method == 'POST':
            Phone_number = request.POST.get('Phone_number')
            email = request.POST.get('email')
            message = request.POST.get('message')
            print(email)
            ContactUs.objects.create(email=email, Phone_number=Phone_number, message=message)
            messages.success(request, 'Your contact request was sent successfully!')
            return redirect('/')
    return render(request, 'core/contact.html')