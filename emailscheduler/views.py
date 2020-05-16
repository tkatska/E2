from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
import threading
from .forms import ContactForm
from .models import Email
import time
import datetime

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            wait_time = form.cleaned_data['time']
            try:
                e = Email(email=email)
                e.save()
                print("Thread starting")
                print(datetime.datetime.now())
                t = threading.Thread(target=send_email_with_sleep(subject, message, email, wait_time))
                t.start()
                t.join() # join without a timeout to verify thread shutdown.
                print("Thread finished")
                print(datetime.datetime.now())
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form})

def send_email_with_sleep(subject, message, email, wait_time):
    time.sleep(wait_time) # send email after X amount of seconds
    send_mail(subject, message, email, ['admin@example.com'])

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

def displayEmailView(request):
    template = loader.get_template('results.html') 
    emailsList = Email.objects.order_by('-id')[0:10]
    print(emailsList)
    email_data = {
        "emailsList": emailsList}    
    return HttpResponse(template.render(email_data, request))
    