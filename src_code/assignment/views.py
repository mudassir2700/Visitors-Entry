from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
import random
from .utils import randomgenerator
from datetime import date, datetime,time,timedelta
from django.http import HttpResponseRedirect
from django.conf import settings

# Create your views here.

def homepage(request):
	obj = Appointment.objects.all()
	#for i in obj:
		#print(str(i.in_time).split(" "))
		#print(i.out_time)
		#print(i.host.email)
	return render(request,'assignment/homepage.html')


def register(request):
	if request.method == 'POST':
		form = UserAdminCreationForm(request.POST or None,request.FILES or None)
		if form.is_valid():
			form.save()
			user,msg=form.save(commit=False)
			if msg=="":
				return render(request,'assignment/mainpage.html')
			else:
				messages.error(request,msg)
				return redirect('assignment:index')
	else:
		form = UserAdminCreationForm()
	return render(request, 'assignment/register.html', {'form': form})


def login_view(request):
	if request.method=='POST':
		form=AuthenticationForm(data=request.POST)
		print(form)
		if form.is_valid():
			print(form)
			user=form.get_user()
			#us=User.objects.all()
			login(request,user)
			return render(request,'assignment/mainpage.html')

	else:
		form = AuthenticationForm()

	return render(request,'assignment/login1.html',{'form':form})


def booking_view(request):
	all_users=Appointment.objects.all()
	all_hosts = User.objects.all()
	all_users_count = Appointment.objects.all().count()
	count_dict={}
	#print(all_users_count)
	for i in range(8):
		count_dict[i]=i+1


	#print(jhdfdfjfkdh)
	if request.method=='POST':
		form = booking(data = request.POST or None)
		print(form)
		print("dsjgsgjsghjg")
		error=[]
		if form.is_valid():
			print('hfdjjhdjhf')
			in_date = form.cleaned_data['in_date']
			out_date = form.cleaned_data['out_date']
			indate_list = str(in_date).split(" ")
			outdate_list = str(out_date).split(" ")
			#print(indate_list)
			#print(hdjhsjfhdhsj)

			for i in all_users:
				intimelst = str(i.in_time).split(" ")
				outtimelst = str(i.out_time).split(" ")
				if (indate_list[0]==intimelst[0] and outtimelst[0]==outdate_list[0]) and ((intimelst[1]>=indate_list[1] and intimelst[1]<=outdate_list[1]) or (outtimelst[1]>=indate_list[1] and outtimelst[1]<=outdate_list[1])):
					error.append('Slot is already full')


			user = form.save(commit=False)
			num = str(user.contact)
			user.in_time=in_date
			user.out_time=out_date
			if(indate_list[0]<str(date.today()) and outdate_list[0]<str(date.today())):
				error.append('Please enter a future date')
			if indate_list[0]!=outdate_list[0]:
				error.append('In time and Out time must be of same date')
			if indate_list[1]>outdate_list[1]:
				error.append('Enter Correct Time')
			if(indate_list[1]<str(datetime.now().strftime("%H:%M:%S")) and indate_list[0]<=str(date.today())):
				error.append('Please enter a future time slot for In Time')
			if(outdate_list[1]<str(datetime.now().strftime("%H:%M:%S")) and outdate_list[0]<=str(date.today())):
				error.append('Please enter a future time slot Out Time')
			if(len(num)!=10):
				error.append('Enter a valid number')
			
			if len(error)>0:
				print(error)
				for each in error:
					messages.error(request,each)
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
			if len(error)==0:

				number = random.randint(0,10000)
				user.booking_id = number

				user.save()
				subject = 'Appointment'
				message ="Name : "+user.name+"\n"+"Contact Number : "+str(user.contact)+'\n'+"Email : "+str(user.email)+'\n'+"In Time : "+str(user.in_time)+'\n'+"Out Time : "+str(user.out_time)+'\n'+"Booking Id : "+str(user.booking_id)
				to_email = user.host.email
				from_email = settings.EMAIL_HOST_USER
				to_list = [to_email,settings.EMAIL_HOST_USER]
				send_mail( subject, message, from_email,to_list,fail_silently=True)
				messages.success(request,'Your booking is complete')
				return redirect('assignment:index')
	else:
		form = booking()
	return render(request,'assignment/booking.html',{'form':form,'count_dict':count_dict,'all_users':all_users,'all_hosts':all_hosts})

def checkout_view(request):
	if request.method=='POST':
		flag=False
		book_id = request.POST.get("bookid")
		try:
			obj = Appointment.objects.get(booking_id=book_id)
			flag = True
		except:
			flag = False
		if flag and obj.meeting_status=='Pending':
			obj.meeting_status = 'Completed'
			obj.save()
			subject = 'Appointment Status'
			message ="Appointment Booking Name : "+obj.name+"\n"+"Contact Number : "+str(obj.contact)+'\n'+"Host Name : "+obj.host.name+'\n'+"In Time : "+str(obj.in_time)+'\n'+"Out Time : "+str(obj.out_time)+'\n'+"Address : "+obj.host.address
			to_email = obj.email
			from_email = settings.EMAIL_HOST_USER
			to_list = [to_email,settings.EMAIL_HOST_USER]
			send_mail( subject, message, from_email,to_list,fail_silently=True)
			messages.success(request,'Your meeting is completed')
			return redirect('assignment:index')
		if not flag:
			messages.error(request,'Please enter Correct Booking Id')
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

	return render(request,'assignment/checkout.html')


