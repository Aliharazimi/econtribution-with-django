from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import Contribution, Contributor, Withdrawal
from .forms import ProfileUpdateForm, RegistrationForm, ContForm, ContributionForm, UserUpdateForm, WithdrawalForm
import random
import string



def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('users:profile', username=user)
            else:
                messages.error(request, 'username and password doesn\'t match')
    return render(request, "users/login.html")


def signout(request):
    logout(request)
    return redirect('index')



def registration(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                first_name = form.cleaned_data.get('first_name')
                email = form.cleaned_data.get('email')
                messages.success(request, f'Account created for {username}!')
                return redirect('users:signin')
        else:
            form = RegistrationForm()
        return render(request, 'users/signup.html', {"form": form})


def profile(request, username):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            _username = u_form.cleaned_data.get('username')
            messages.success(request, 'Your account has been updated!')
            return redirect('users:profile', username=_username)
    elif request.user.is_authenticated:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)




    contribution = Contribution.objects.filter(user__username=username)
    user_profile = User.objects.get(username__exact=username)
    if request.method == 'POST':
        form = ContributionForm(request.POST or None)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.user = user_profile
            contribution.save()
            messages.success(request, 'your task was successfully Added!')
            return redirect('users:profile', username=username)
    elif request.user.is_authenticated:
        form = ContributionForm()
        context = {
                'contribution': contribution,
                'taskform': form,
                "cuser": user_profile,
                "u_form": u_form,
                "p_form": p_form
            }
    else:
        context = {
                'contribution': contribution,
                "cuser": user_profile,
            }
    return render(request, 'users/profile.html', context)

def contributions(request, username):
    contribution = Contribution.objects.filter(user__username=username).order_by('-created')
    user_profile = User.objects.get(username__exact=username)
    context = {
            'contribution': contribution,
            "cuser": user_profile
        }
    return render(request, 'users/contributions.html', context)

def create_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def get_contribution(request, slug):
    contcount = Contributor.objects.filter(contribution__slug=slug)
    user_profile = User.objects.get(contribution__slug=slug)
    form = ContForm(request.POST or None)
    cont = get_object_or_404(Contribution, slug=slug)
    rcont = Contribution.objects.filter(slug=slug)
    rcontributor = Contributor.objects.filter(contribution__slug=slug, status="paid").order_by('-created')


    if request.method == 'POST':
            if form.is_valid():
                id = create_id()
                temp = form.save(commit=False)
                temp.contribution = cont
                temp.transaction_id = id
                temp = Contribution.objects.get(slug=slug)
                temp.contributor_count += 1
                amount = form.cleaned_data.get('amount_deposited')
                form.save()
                temp.save()
                # temp.amount_contributed += amount
                messages.success(request, "Contribution Added Successfully")
                return redirect(f'https://pay.insolify.com/pay/wed/{id}/{amount}')                         
    else:
        form = ContForm()
    context = {
            "rcont": rcont,
            "cont": cont,
            "cform": form,
            "rcontributor": rcontributor,
            "contcount": contcount,
            "cuser": user_profile
            }
    return render(request, "users/cont_profile.html", context)

def widthdrawal(request, slug):
    withdrawal_cont = Withdrawal.objects.filter(contribution__slug=slug)
    user_profile = User.objects.get(contribution__slug=slug)
    form = WithdrawalForm(request.POST or None)
    cont = get_object_or_404(Contribution, slug=slug)
    rcont = Contribution.objects.filter(slug=slug)
    widthdrawal = Withdrawal.objects.filter(contribution__slug=slug, status="successful").order_by('-created')
    rcontributor = Contributor.objects.filter(contribution__slug=slug, status="paid").order_by('-created')


    if request.method == 'POST':
            if form.is_valid():
                withdrawal = form.save(commit=False)
                withdrawal.contribution = cont
                withdrawal = Contribution.objects.get(slug=slug)
                id = withdrawal.id
                amount = form.cleaned_data.get('amount')
                form.save()
                withdrawal.save()
                messages.success(request, "Your withdrawal request was submited Successfully!")
                return redirect(f'https://pay.insolify.com/wed/{id}/{amount}')                         
    else:
        form = WithdrawalForm()
    context = {
            "rcont": rcont,
            'withdrawal_cont': withdrawal_cont,
            "cont": cont,
            "cform": form,
            "widthdrawals": widthdrawal,
            "cuser": user_profile,
            'rcontributor': rcontributor
            }
    return render(request, "users/widrawal_page.html", context)