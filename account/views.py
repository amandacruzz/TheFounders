from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail, EmailMessage
import random
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from .models import *
import re


# Create your views here.

@csrf_exempt
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('dashboard')
		else:
			messages.info(request, 'Invalid Credentials')
			return render(request, 'login.html')
	else:
		return render(request, 'login.html')

@csrf_exempt
def createacc(request):
	emailPattern = re.compile("([\w\.\-])+@([\w\.\-])+\.(\w)+")  # match if there's an @ and a . with something follows
	usernamePattern = re.compile("\w\w\w\w\w\w(\w)*")  # match if there's 6 or more alphanumeric (with _) characters
	passwordSpecialChar = re.compile("(.)*([!@#\$%\^&\*\?_])(.)*")  # checks password if there's a special character
	passwordUpperChar = re.compile("([\w!@#\$%\^&\*\?])*([A-Z])([\w!@#\$%\^&\*\?])*")  # matches if there's a capital letter

	if request.method == 'POST':
		email = request.POST['email']
		username = request.POST['username']
		password = request.POST['password']
		password2 = request.POST['password2']

		if not emailPattern.match(email):
			messages.info(request, 'Invalid Email')
			return render(request, 'create_acc.html')
		elif not usernamePattern.match(username):
			messages.info(request, 'Username Needs To Be 6 Or More Alphanumeric Characters')
			return render(request, 'create_acc.html')
		elif not passwordSpecialChar.match(password) or not passwordUpperChar.match(password) or len(password) < 8:
			messages.info(request, '''Password Needs To Have At Least One Capital Letter, 
									One Special Character, and be At Least 8 Characters Long''')
			return render(request, 'create_acc.html')

		if password == password2:
			if User.objects.filter(username=username).exists():
				messages.info(request, 'Username Already Exists')
				return render(request, 'create_acc.html')
			elif User.objects.filter(email=email).exists():
				messages.info(request, 'Email Already Exists')
				return render(request, 'create_acc.html')
			else:
				user = User.objects.create_user(username=username, password=password, email=email)
				user.save()
				return redirect('login')
		else:
			messages.info(request, "Passwords Do Not Match")
			return render(request, 'create_acc.html')
	else:
		return render(request, 'create_acc.html')

@csrf_exempt
def logout(request):
	auth.logout(request)
	return redirect('/')
@csrf_exempt
def sendResetEmail(email, secretNum, username):
	template = "reset_email.html"

	url = "http://hextrack.app/account/reset"

	email_contents = render_to_string(template, {'secret': secretNum, 'user': username, 'url': url})
	print(email_contents)
	message = EmailMessage('HexTrack Password Reset', email_contents, 'accounts@hextrack.app', [email])
	message.content_subtype = 'html'
	message.send()
@csrf_exempt
def forgotpass(request):
	emailPattern = re.compile("([\w\.\-])+@([\w\.\-])+\.(\w)+")  # match if there's an @ and a . with something follows
	usernamePattern = re.compile("\w\w\w\w\w\w(\w)*")  # match if there's 6 or more alphanumeric (with _) characters
	passwordSpecialChar = re.compile("(.)*([!@#\$%\^&\*\?_])(.)*")  # checks password if there's a special character
	passwordUpperChar = re.compile("([\w!@#\$%\^&\*\?])*([A-Z])([\w!@#\$%\^&\*\?])*")  # matches if there's a capital letter

	if request.method == 'POST':
		email = request.POST['email']
		username = request.POST['username']
		password = request.POST['password']
		password2 = request.POST['password2']

		if not emailPattern.match(email):
			messages.info(request, 'Invalid Email')
			return render(request, 'forgot_pass.html')
		elif not usernamePattern.match(username):
			messages.info(request, 'Username Needs To Be 6 Or More Alphanumeric Characters')
			return render(request, 'forgot_pass.html')
		elif not passwordSpecialChar.match(password) or not passwordUpperChar.match(password) or len(password) < 8:
			messages.info(request, '''Password Needs To Have At Least One Capital Letter, 
										One Special Character, and be At Least 8 Characters Long''')
			return render(request, 'forgot_pass.html')

		if password == password2:
			if not User.objects.filter(username=username).exists() or not User.objects.filter(email=email).exists():
				messages.info(request, 'Invalid Email or Username')
				return render(request, 'forgot_pass.html')
			else:
				secretNum = random.randint(0, 1000000000)
				user = User.objects.get(username=username)
				changeRequests = Acc_Pass_Change.objects.filter(username_id=user)

				if len(changeRequests) != 0: # if the user makes a new change request delete the old requests
					for i in changeRequests:
						i.delete()

				changeReq = Acc_Pass_Change(username_id=user, email=email, secretInt=secretNum, newPassword=password)
				changeReq.save()

				sendResetEmail(email, secretNum, username)

				messages.info(request, 'Check Your Email For The Reset Link')
				render(request, "forgot_pass.html")
		else:
			messages.info(request, "Passwords Do Not Match")
			return render(request, 'create_acc.html')

	return render(request, "forgot_pass.html")

@csrf_exempt
def reset(request):
	secretInt = request.GET['k']
	username = request.GET['u']

	user = User.objects.get(username=username)
	pass_request = Acc_Pass_Change.objects.filter(username_id=user)

	if len(pass_request) > 1:  # you're not supposed to be able to make multiple requests
		for i in pass_request:
			i.delete()
	elif len(pass_request) == 1:
		pass_request = pass_request[0]

		if int(secretInt) == pass_request.secretInt:  # random int matches, meaning that request is approved
			user.set_password(pass_request.newPassword)
			user.save()

		pass_request.delete()   # since the pass request gets deleted regardless of match, brute force won't work since
								# after one try the request is deleted
	messages.info(request, "Password Has Been Reset")
	return redirect('login')
