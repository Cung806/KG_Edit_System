from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
import account


# @login_required
def logout_view(request):
    request.session.clear()
    # auth.logout(request)
    return redirect('../')
    # Redirect to a success page.


def index(request):
    if 'is_login' in request.session:
        return render(request, 'graph.html')
    return render(request, "login.html")


def show_demo(request):
    return render(request,"graph_demo.html")

# def login_success(request):
#     return render(request, 'graph.html')


def login_view(request):
    print("a")
    user_name = request.POST.get('username')
    password = request.POST.get('password')
    domainname = request.POST.get('domain')
    user = authenticate(username =user_name, password=password)
    user_domain_list = []
    if user:
        authuser = account.models.User.objects.get(username=user_name)
        domain_set = authuser.domainmodel_set.all()
        for x in domain_set:
            user_domain_list.append(x.domain_name)
        if domainname in user_domain_list:
            request.session["username"] = user_name
            request.session["domain_name"] = domainname
            request.session['is_login'] = True
            return HttpResponse('SUCCESS')
        else:
            return HttpResponse("DOMAIN FAIL")
    else:

        return HttpResponse("USER FAIL")

