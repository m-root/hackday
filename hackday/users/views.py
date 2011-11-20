from users.forms import SignUpForm,  SignInForm
from users.models import User, UserProfile, Tshirt, Diet, Location
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader


def index(request):
    users = User.objects.order_by('last_name').order_by('first_name').order_by('username')

    t = loader.get_template('users/index.html')
    c = RequestContext(request, {
        'users': users
    })

    return HttpResponse(t.render(c))


def sign_up(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                    form.cleaned_data['user_name'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password'])

            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # Create the user profile
            user_profile = UserProfile(
                    user=user,
                    tshirt=form.cleaned_data['tshirt'],
                    diet=form.cleaned_data['diet'],
                    location=form.cleaned_data['location'],
                    description=form.cleaned_data['description'])
            user_profile.save()

            # Log the user in
            user = authenticate(username=user.username,
                    password=form.cleaned_data['password'])
            login(request, user)

            return HttpResponseRedirect('/users') # Redirect after POST
    else:
        form = SignUpForm()

    t = loader.get_template('users/signup.html')
    c = RequestContext(request, {
        'form': form,
    })

    return HttpResponse(t.render(c))


def sign_out(request):

    logout(request)

    t = loader.get_template('users/signout.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))


def sign_in(request):
    error_message = None

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['user_name'],
                    password=form.cleaned_data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/users')
                else:
                    error_message = "Account disabled"
            else:
                error_message = "Bad username or password"
    else:
        form = SignInForm()

    t = loader.get_template('users/signin.html')
    c = RequestContext(request, {
        'form': form,
        'error_message': error_message,
    })
    return HttpResponse(t.render(c))


def profile(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)

    t = loader.get_template('users/profile.html')
    c = RequestContext(request, {
        'user_': user,
        'user_profile': user_profile,
    })
    return HttpResponse(t.render(c))
