from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from .models import Questions,phone_no
from .task_celery import test_fun
from datetime import timedelta
from django.utils import timezone
# Create your views here.
def register(request):
    # print('abc')
    if request.method == 'POST':
        print('a')
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        phone = request.POST['phone']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                print('a')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                print('b')
                messages.info(request,'email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email = email,password= password)
                user.save()
                ph = phone_no(user = user,phoneno = phone)
                ph.save()
                messages.info(request,'user created')
                return redirect('login')
        else :
            messages.info(request,'password not match')
            return redirect('register')
    else:
      
        return render(request,'accounts/register.html')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username,password = password)
        print(user)
        if user != None:
            auth.login(request,user)
            return redirect('homepage')
        else :
            print('here')
            messages.info(request,'invalid credentials')
            return redirect('login')

    else :
        redirect('/')
        return render(request,'accounts/login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
def homepage(request):
    Questions.objects.filter(date_created__lte=timezone.now()-timedelta(minutes=2))
    print(Questions.objects.filter(date_created__lte=timezone.now()-timedelta(minutes=2)))
    question = Questions.objects.all()
    return render(request,'dashboard/homepage.html',{'questions' : question})
def profilepage(request):
    profile = User.objects.get(username= request.user)
    dummy = phone_no.objects.get(user= request.user)
    poll = Questions.objects.all

    data = {
        "username": profile,
        "email": profile.email,
        "phone": dummy.phoneno,
        "poll" : poll
    }
    return render(request,'dashboard/profilepage.html',{'data':data})
def question(request):
    if request.method == 'POST':
        print(request.user)
        #print(phone_no.objects.get(user = request.user).ques_can_add)
        dummy = phone_no.objects.get(user =request.user)
        print(dummy.ques_can_add)
        if dummy.ques_can_add != 0: 
            question = request.POST['question']
            option1 = request.POST['opt1']
            option2 = request.POST['opt2']
            option3 = request.POST['opt3']
            option4 = request.POST['opt4']
            us = request.user
            dummy.ques_can_add = dummy.ques_can_add-1
            dummy.save()
            ques = Questions(user= us,question = question,option1 = option1,option2 = option2,option3 = option3,option4 = option4)
            ques.save()
            
            messages.info(request,'question created')
            return render(request,'dashboard/homepage.html')
        else:
            messages.info(request,'you maximum limit over to make a questions!')
            return render(request,'dashboard/homepage.html')
    else:
        return render(request,'dashboard/question_page.html')
def vote(request,poll_id):
    poll = Questions.objects.get(id = poll_id)
    if poll.visited == True:
        messages.info(request,'you already visted')
        return redirect('homepage')
    elif request.method == 'POST':
        a = request.POST['options-outlined']
        question = Questions.objects.all()
        if a == poll.option1:
            poll.option1_count = poll.option1_count+1
            poll.save()
        elif a== poll.option2:
            poll = poll.option2_count+1
            poll.save()
        elif a == poll.option3:
            poll.option3_count = poll.option3_count+1
            poll.save()
        else :
            poll.option4_count = poll.option4_count+1
            poll.save()  
        poll.visited = True
        poll.save()
        return render(request,'dashboard/homepage.html',{'questions':question})
    else:
        return render(request,'dashboard/vote.html',{'poll':poll})
def result(request,poll_id):
    poll = Questions.objects.get(id = poll_id)
    return render(request,'dashboard/result.html',{'poll':poll})