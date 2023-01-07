from django.shortcuts import render
from .models import Contact, Message

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        if request.user.is_authenticated:
            customer = request.user.customer
            name = f"{request.user.first_name} {request.user.last_name}" if request.user.first_name and request.user.last_name else request.user.username
            email = request.user.email 
            Message.objects.create(customer = customer, name = name, email = email, subject = subject, message = message)
        else:
            Message.objects.create(name = name, email = email, subject = subject, message = message)
    context = {
        "contact": Contact.objects.first()
    }
    return render(request, 'contact.html', context)