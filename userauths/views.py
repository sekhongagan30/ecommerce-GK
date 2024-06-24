from django.shortcuts import redirect, render
from userauths.forms import UserRegisterationForm, ProfileForm, AddressForm
from django.contrib.auth import login, logout, authenticate
from userauths.models import Profile
from core.models import Address
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import User
# User = settings.AUTH_USER_MODEL
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.core.mail import send_mail
from django.conf import settings
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }

# Create your views here.

def send_mail_after_registration(recipient_user, auth_token):
    subject = 'Testing Mail'
    msg = f'Hi paste the link to verify your account http://127.0.0.1:8000/user/verify/{auth_token}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_user]

    send_mail(subject, msg, from_email, recipient_list)

def success(request):
    return render(request , 'userauths/success.html')

def token_send(request):
    return render(request , 'userauths/token_send.html')

def error_page(request):
    return  render(request , 'userauths/error.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('userauths:sign-in')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('userauths:sign-in')
        else:
            return redirect('userauths:error')
    except Exception as e:
        print(e)
        return redirect('core:indexOfHomePage')



class RegisterApi(APIView):
    http_method_names = ['get', 'post']
    renderer_classes = (JSONRenderer,)
    def get(selfself, request):
        form = UserRegisterationForm()
        context = {
            'form': form,
        }
        return render(request, 'userauths/sign-up.html', context)
    def post(self, request): # rollback changes
        form = UserRegisterationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            ###send mail
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            print("ggn 88", auth_token)
            send_mail_after_registration(email, auth_token)
            return redirect('userauths:token_send')
            ###send mail

                # # these messages are shown in admin url
                # messages.success(request, f"Hey {username}, your account has been created successfully.")
                # new_user = authenticate(username=form.cleaned_data['email'], password = form.cleaned_data['password1']) # Password is password1, confirm password is password2
                # login(request, new_user)
                # # token = get_tokens_for_user(new_user)
                # # print("ggn 33", token)
                # # in below line, space after : is strictly not allowed
                # return redirect("core:indexOfHomePage") # value which we passed in core is name which is written for urlPatterns:path in urls.py of key"core"

        context = {
            'form': form,
        }
        return render(request, 'userauths/sign-up.html', context)


class LoginApi(APIView):
    http_method_names = ['get', 'post']
    renderer_classes = (JSONRenderer,)
    def get(self, request):
        if request.user.is_authenticated: # agr pehle login kia hua hai and browser mai login history hai, then user is logged in user ka email, and isAuthenticated=True
            messages.warning(request, "Hey, you are already logged in !")
            return redirect("core:indexOfHomePage")
        context = {}
        return render(request, "userauths/sign-in.html", context)
    def post(self, request):
        if request.user.is_authenticated: # agr pehle login kia hua hai and browser mai login history hai, then user is logged in user ka email, and isAuthenticated=True
            messages.warning(request, "Hey, you are already logged in !")
            return redirect("core:indexOfHomePage")

        email = request.POST.get("email")
        password = request.POST.get("password") # the thing we write in get("") is name of <input> we write in html
        try:
            user_obj = User.objects.filter(email=email).first()
            if user_obj is None:
                messages.warning(request, 'User not found !')
                return redirect("userauths:sign-in")
            profile_obj = Profile.objects.filter(user=user_obj).first()
            if not profile_obj.is_verified:
                messages.warning(request, 'Profile is not verified. Please check email !')
                return redirect("userauths:sign-in")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                # token = get_tokens_for_user(user)
                # print("ggn 60", token)
                return redirect("core:indexOfHomePage")
            else:
                messages.warning(request, "User does not exists. Create an account.")
        except:
            messages.warning(request, f"User with {email} does not exist")

        context = {}
        return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.warning(request, "You logged out.")
    return redirect("userauths:sign-in")

@login_required
def view_profile(request):
    if request.method=='POST':
        address = request.POST['address']
        mobile = request.POST['mobile']
        new_address = Address.objects.create(
            user=request.user,
            address = address,
            mobile = mobile,
            status = False
        )
        messages.success(request, "Address added successfully")
        return redirect("userauths:profile")
    profile = Profile.objects.filter(user=request.user)
    addressForm =AddressForm()
    context = {
        "profile": profile,
        'addressForm': addressForm
    }
    return render(request, 'userauths/profile.html', context)

class ProfileUpdateView(APIView): # login required
    http_method_names = ['get', 'post']
    renderer_classes = (JSONRenderer,)
    def get(self, request):
        print("ggn 177", request.user, request.user.is_authenticated)
        userProfile = Profile.objects.filter(user=request.user)
        if userProfile:
            userProfile = userProfile[0]
        if userProfile:
            form = ProfileForm(instance=userProfile) # instance attr will auto fill the data with given data
        else:
            form = ProfileForm()
        context = {
            'form': form,
            'profile': userProfile
        }
        return render(request, 'userauths/profile-edit.html', context)

    def post(self, request):
        userProfile = Profile.objects.filter(user=request.user)
        if userProfile:
            userProfile = userProfile[0]
        if userProfile:
            form = ProfileForm(request.POST, request.FILES, instance=userProfile)
        else:
            form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save() # update krna hai
            messages.success(request, "Profile Updated Successfully.")
            return redirect("userauths:profile")
        context = {
            'form': form,
            'profile': userProfile
        }
        return render(request, 'userauths/profile-edit.html', context)
