from django.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from account.models import User

from django import forms
from firebase import firebase
import csv



db = firebase.FirebaseApplication("https://slimbydesignios-b7a28.firebaseio.com", None)
secret="gbuTPGUqQPtUJf7jD3eJ14olWj33eGB59MIXaCvA"
auth=firebase.FirebaseAuthentication(secret,"slimbydesignapp@gmail.com")
db.authentication = auth

restaurants = db.get('/establishments', None)
restaurant_array = [None] * len(restaurants)
reviews = db.get('/reviews', None)
review_array = [None] * len(reviews)
homes = db.get('/home', None)
home_array = [None] * len(homes)

# Create your views here.
# class UserForm(forms.Form):
#     username = forms.CharField(label='username:',max_length=100)
#     password = forms.CharField(label='password:',widget=forms.PasswordInput())
    # widget = forms.PasswordInput())
class UserForm(forms.Form):
    username = forms.CharField(label='username:', max_length=100)
    password = forms.CharField(label='password:', widget=forms.PasswordInput())

# class UserLoginForm(forms.Form):
#     username = forms.CharField(label='username:',max_length=100)
#     password = forms.CharField(label='password:',widget=forms.PasswordInput())

class FilterForm(forms.Form):
    name = forms.CharField(label='Name:',max_length=100)
    location_type = forms.CharField(label='Type:',max_length=100)
    lowest_rating = forms.CharField(label='Lowest Rating:',max_length=5)
    highest_rating = forms.CharField(label='Highest Rating:',max_length=5)
    city = forms.CharField(label='City:',max_length=100)
    state = forms.CharField(label='State:',max_length=100)

# def register(request):
#     if request.method == "POST":
#         uf = UserForm(request.POST)
#         if uf.is_valid():
#             #Get the information from form
#             username = uf.cleaned_data['username']
#             password = uf.cleaned_data['password']
#             email = uf.cleaned_data['email']
#             #Write data to the database
#             user = User()
#             user.username = username
#             user.password = password
#             user.email = email
#             user.save()
#             #return the success.html
#             return render(request, 'success.html',{'username':username})
#     else:
#         uf = UserForm()
#         return render(request, 'register.html',{'uf':uf})

# def login(req):
#     if req.method == 'POST':
#         uf = UserLoginForm(req.POST)
#         if uf.is_valid():
#             #Get the username and password of form
#             username = uf.cleaned_data['username']
#             password = uf.cleaned_data['password']
#             #Compare the username and password of form with the account data in database
#             user = User.objects.filter(username__exact = username,password__exact = password)
#             if user:
#                 #If success, return to the index.html
#                 response = HttpResponseRedirect('/account/index/')
#                 #write the username into cookie, the duration time is 3600 s
#                 response.set_cookie('username',username,3600)
#                 return response
#             else:
#                 #If the username is invalid, still stay at the login.html
#                 return HttpResponseRedirect('/account/ErrorMessageAfterLogin/')
#     else:
#         uf = UserLoginForm()
#     return render(req, 'login.html',{'uf':uf})

def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
       
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
          
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                return HttpResponseRedirect('/account/review/')
            else:
                return render(request,'fail.html',{'username':username})
    else:
        uf = UserForm()
    return render(request,'login.html',{'uf':uf})

# def ErrorMessageAfterLogin(req):
#     if req.method == 'POST':
#         uf = UserLoginForm(req.POST)
#         if uf.is_valid():
#             #Get the username and password of form
#             username = uf.cleaned_data['username']
#             password = uf.cleaned_data['password']
#             #Compare the username and password of form with the account data in database
#             user = User.objects.filter(username__exact = username,password__exact = password)
#             if user:
#                 #If success, return to the index.html
#                 response = HttpResponseRedirect('/account/index/')
#                 #write the username into cookie, the duration time is 3600 s
#                 response.set_cookie('username',username,3600)
#                 return response
#             else:
#                 #If the username is invalid, still stay at the login.html
#                 return HttpResponseRedirect('/account/ErrorMessageAfterLogin/')
#     else:
#         uf = UserLoginForm()
#     return render(req, 'ErrorMessageAfterLogin.html',{'uf':uf})

#successful login
def index(req):
    return render(req, 'review.html' )

#Logout
def logout(req):
    response = HttpResponse('logout !!')
    #clean the usernames in the cookies
    response.delete_cookie('username')
    return render('login.html')

def filter(req):
    uf = FilterForm()
    return render(req, 'filter.html',{'uf':uf})

def table(req):
    i = 0
    for key, value in restaurants.items():
        x = {}
        x['city'] = value['city']
        x['name'] = value['name']
        x['numRates'] = value['numRates']
        x['rating'] = value['rating']
        x['type'] = value['type']
        restaurant_array[i] = x
        i+=1
    i = 0
    for key, value in reviews.items():
        x = {}
        x['answer1'] = value['answer1']
        x['answer2'] = value['answer2']
        x['answer3'] = value['answer3']
        x['answer4'] = value['answer4']
        x['answer5'] = value['answer5']
        x['answer6'] = value['answer6']
        x['answer7'] = value['answer7']
        x['answer8'] = value['answer8']
        x['answer9'] = value['answer9']
        x['answer10'] = value['answer10']
        x['city'] = value['city']
        x['date'] = value['date']
        x['day'] = value['day']
        x['name'] = value['name']
        x['rating'] = value['rating']
        x['time'] = value['time']
        x['type'] = value['type']
        review_array[i] = x
        i+=1

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="test.csv"'

    writer = csv.writer(response)
    for entry in restaurant_array:
        writer.writerow(entry.values())
    return render(req, 'index.html', {'table': restaurant_array, 'reviews': review_array})

def restaurant(req):
    i = 0
    for key, value in restaurants.items():
        x = {}
        x['city'] = value['city']
        x['name'] = value['name']
        x['numRates'] = value['numRates']
        x['rating'] = value['rating']
        x['type'] = value['type']
        restaurant_array[i] = x
        i+=1
    return render(req, 'restaurant.html', {'table': restaurant_array})

def review(req):
    i = 0
    for key, value in reviews.items():
        x = {}
        x['date'] = value['date']
        x['time'] = value['time']
        x['day'] = value['day']
        x['city'] = value['city']
        x['name'] = value['name']
        x['rating'] = value['rating']
        x['type'] = value['type']
        x['answer1'] = value['answer1']
        x['answer2'] = value['answer2']
        x['answer3'] = value['answer3']
        x['answer4'] = value['answer4']
        x['answer5'] = value['answer5']
        x['answer6'] = value['answer6']
        x['answer7'] = value['answer7']
        x['answer8'] = value['answer8']
        x['answer9'] = value['answer9']
        x['answer10'] = value['answer10']
        x['answer11'] = value['answer11']
        x['answer12'] = value['answer12']
        x['answer13'] = value['answer13']
        x['answer14'] = value['answer14']
        review_array[i] = x
        i+=1
    return render(req, 'review.html', {'table': review_array})

def home(req):
    i = 0
    for key, value in homes.items():
        x = {}
        x['date'] = value['date']
        x['time'] = value['time']
        x['day'] = value['day']
        x['city'] = value['city']
        x['rating'] = value['rating']
        x['type'] = value['type']
        x['answer1'] = value['answer1']
        x['answer2'] = value['answer2']
        x['answer3'] = value['answer3']
        x['answer4'] = value['answer4']
        x['answer5'] = value['answer5']
        x['answer6'] = value['answer6']
        x['answer7'] = value['answer7']
        x['answer8'] = value['answer8']
        x['answer9'] = value['answer9']
        x['answer10'] = value['answer10']
        home_array[i] = x
        i+=1
    return render(req, 'home.html', {'table':home_array})




def restaurant_csv(req):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="restaurant_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['City', 'Name', 'Number of Ratings', 'Rating', 'Type'])
    if (restaurant_array[0] is not None ):
        for entry in restaurant_array:
            writer.writerow(entry.values())
        return response
    else :
        restaurant(req)
        return HttpResponseRedirect('../restaurant')

def review_csv(req):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="review_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Time', 'Day', 'City', 'Name', 'Rating', 'Type', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10','Q11', 'Q12', 'Q13', 'Q14'])
    if (review_array[0] is not None):
        for entry in review_array:
            writer.writerow(entry.values())
        return response
    else:
        review(req)
        return HttpResponseRedirect('../review')

def home_csv(req):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="home_data.csv"'
        writer = csv.writer(response)
        writer.writerow(
            ['Date', 'Time', 'Day', 'City', 'Rating', 'Type', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8',
             'Q9', 'Q10'])
        if (home_array[0] is not None):
            for entry in home_array:
                writer.writerow(entry.values())
            return response
        else:
            home(req)
            return HttpResponseRedirect('../home')
# def graph(req):
#     return render_to_response(req, 'graph.html',)

# def graph(request):
#     return render(request,
#     'graph.html',
#     )




