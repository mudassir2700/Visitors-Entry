from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)





class UserManager(BaseUserManager):
	def create_user(self,email,name,role,sex,department,address, password=None):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')
		if not name:
			raise ValueError('Users must have an Name')
		if not role:
			raise ValueError('Users must have a role')
		
		if not address:
			raise ValueError('Users must have Valid Address')


		user = self.model(
			email=self.normalize_email(email),
			name=name,
			role=role,
			department=department,
			address=address,
			sex=sex,
			
			

		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_staffuser(self,email,name,role,sex,department,address, password):
		"""
		Creates and saves a staff user with the given email and password.
		"""
		user = self.create_user(
			email=email,
			password=password,
			name=name,
			role=role,
			department=department,
			address=address,
			sex=sex,
			

		)
		user.staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self,email,name,role,sex,department,address,password):
		"""
		Creates and saves a superuser with the given email and password.
		"""
		user = self.create_user(
			email=email,
			password=password,
			name=name,
			role=role,
			department=department,
			address=address,
			sex=sex,
		)
		user.staff = True
		user.admin = True
		user.active= True
		user.save(using=self._db)
		return user



class User(AbstractBaseUser):

	Male='Male'
	Female='Female'

	gender=(
		(Male,'Male'),
		(Female,'Female'),
		)

	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	name= models.CharField(max_length=255,default=None)
	role= models.CharField(max_length=255,default=None)
	sex=models.CharField(choices=gender,max_length=20,default=None)
	department= models.CharField(max_length=255,default=None)
	address = models.CharField(max_length=255,default=None)
	active = models.BooleanField(default=False)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False) 

	objects = UserManager()


	USERNAME_FIELD = 'email'

	REQUIRED_FIELDS = ['name','role','department','sex','address'] 
	def get_full_name(self):
		# The user is identified by their email address
		return self.email

	def get_short_name(self):
		temp = self.email+','+self.name+','+self.department
		return temp

	def __str__(self):
		temp = self.email+','+self.name+','+self.department
		return temp

	def has_perm(self, perm, obj=None):
		
		return True

	def has_module_perms(self, app_label):
		
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		return self.staff

	@property
	def is_admin(self):
		"Is the user a admin member?"
		return self.admin

	@property
	def is_active(self):
		"Is the user active?"
		return self.active


class Appointment(models.Model):
	name = models.CharField(max_length=255,default=None)
	email = models.EmailField(max_length=255,default=None)
	contact = models.BigIntegerField(default=None,max_length=10)
	in_time = models.DateTimeField(auto_now_add=False,auto_now=False)
	out_time = models.DateTimeField(auto_now=False,auto_now_add=False)
	host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='Host_Details')
	booking_id = models.PositiveIntegerField(blank=True,default=0)
	meeting_status = models.CharField(blank=True,default='Pending',max_length=255)

	def __str__(self):
		return self.name
