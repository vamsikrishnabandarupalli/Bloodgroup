import base64
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
import cv2
import os
import numpy as np
# Create your views here.
#displaying a home page
def home(request):
    return render(request, 'home.html')

#login page
def login(request):
    #form Authentication for login
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == "POST"):
        un = request.POST['username']
        pw = request.POST['password']
        user = authenticate(request,username=un,password=pw)
        if(user is not None):
            return redirect('/bloodgroup')
        else:
            msg = 'Invalid username or password'
            form = AuthenticationForm()
            return render(request,'login.html',{'form':form,'msg':msg})
    else:
        form = AuthenticationForm()
        return render(request,'login.html',{'form':form})
    
#Registration Page
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
    

#Profile page   
def bloodgroup(request):
    if(request.method == "POST"):
        if(request.FILES.get('abd')):
            # Read the uploaded image file
            # Read the uploaded image file
            img_file = request.FILES['abd']
            img_name = img_file.read()

            img_en = base64.b64encode(img_name).decode('utf-8')
            img_url = f"data:image/jpeg;base64,{img_en}"

            # Decode the image data to a NumPy array
            nparr = np.frombuffer(img_name, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


            # Convert the image to grayscale
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply Gaussian blur to reduce noise
            blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

            # Enhance the contrast using histogram equalization
            enhanced_img = cv2.equalizeHist(blurred_img)

            # Apply Otsu's thresholding
            _, threshold_img = cv2.threshold(enhanced_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Perform morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            morph_img = cv2.morphologyEx(threshold_img, cv2.MORPH_OPEN, kernel)
            morph_img = cv2.morphologyEx(morph_img, cv2.MORPH_CLOSE, kernel)

            # Encode the processed image back to base64
            _, buffer = cv2.imencode('.jpg', morph_img)
            encoded_img = base64.b64encode(buffer).decode('utf-8')
            img_url = f"data:image/jpeg;base64,{encoded_img}"


            # Find contours
            contours, _ = cv2.findContours(threshold_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            total_length = len(contours)


            # Return the image URL and the contour lengths to the template
            return render(request, 'bloodgroup.html', {'img_name' : img_file, 'img': img_url, 'total_length' : total_length })
        else:
            return render(request, 'bloodgroup.html')
    else:
        return render(request, 'bloodgroup.html')