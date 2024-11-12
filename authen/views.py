from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate


# Create your views here.
def home(request):
    return render(request, 'home.html')

def login(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == "POST"):
        un = request.POST['username']
        pw = request.POST['password']
        user = authenticate(request,username=un,password=pw)
        if(user is not None):
            return redirect('/bloodgroup')
        else:
            msg = 'Invalid username/password'
            form = AuthenticationForm()
            return render(request,'login.html',{'form':form,'msg':msg})
    else:
        form = AuthenticationForm()
        return render(request,'login.html',{'form':form})
def registration(request):
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            un = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password1')
            authenticate(username=un,password=pw)
            return redirect('/login')
        else:
            return render(request,'registration.html',{'form':form})
    else:
        form = UserCreationForm()
        return render(request,'registration.html', {'form':form})
    
def bloodgroup(request):
        if(request.method=='POST'):
            img_name = request.FILES.get('abd')
            print(img_name)
            return render(request,'bloodgroup.html',{'img':img_name})
        else:
            return render(request, 'bloodgroup.html')