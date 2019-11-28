import random
from .models import Appointment
def randomgenerator(flag=False):
	random_num=random.randint(0,10000)
	objall=Appointment.objects.all()
	for i in objall:
		#print(i.company_id)
		if i.booking_id==random_num:
			flag=True
			break
	if flag:
		return randomgenerator(flag=False)
	if not flag:
		return random_num
