from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserLoginForm, UserSignUpForm


def login_view(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('email')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Has iniciado sesion correctamente')
            return redirect('network:home')
        else:
            messages.warning(
                request, 'Correo Electronico o Contrasena invalida')
            return redirect('network:home')

    messages.error(request, 'Formulario Invalido')
    return redirect('network:home')


def signup_view(request):
    signup_form = UserSignUpForm(request.POST or None)
    if signup_form.is_valid():
        email = signup_form.cleaned_data.get('email')
        first_name = signup_form.cleaned_data.get('first_name')
        last_name = signup_form.cleaned_data.get('last_name')
        password = signup_form.cleaned_data.get('password')
        try:
            user = get_user_model().objects.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password),
                is_active=True
            )
            login(request, user)
            return redirect('users:profile')

        except Exception as e:
            print(e)
            return JsonResponse({'detail': f'{e}'})


def logout_view(request):
    logout(request)
    return redirect('network:home')


@login_required(login_url='network:home')
def profile_view(request):
    return render(request, 'user/profile.html')


def user_detail(request, slug):
    user = get_object_or_404(get_user_model(), slug=slug)
    is_follower = False
    try:
        if user.is_follower(request.user):
            is_follower = True
    except:
        messages.warning(
            request, 'Debes Iniciar sesion para mas funcionalidades')

    return render(request, 'user/user_detail.html', {'user_detail': user, "is_follower": is_follower})


@login_required(login_url='network:home')
def follow(request, slug):
    to_follow = get_object_or_404(get_user_model(), slug=slug)
    if to_follow.is_follower(request.user):
        to_follow.followers.remove(request.user)
    else:
        to_follow.followers.add(request.user)
    to_follow.save
    return redirect(to_follow)
