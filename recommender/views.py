import datetime
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, Http404
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from django.core import serializers
from .models import Movie, Review, Member
from .forms import SignupForm
import numpy as np

########################################################################################################
#login

#called by button press or url 
#render login page which sends post requests to signUp or Login
def signIn(request):
    signupForm = SignupForm()
    return render(request, 'movies/login.html', {"signupForm" : signupForm})

#if Signing up check the form, create a member then send request on to logIn
def signUp(request):
    if request.method=='POST':
        form = SignupForm(request.POST, request.FILES)        
        
        if form.is_valid():
            p = request.POST
            member =  Member(username=p['email'], name=p['name'], dob=p['dob'], gender=p['gender'], email=p['email'])
            member.set_password(p['password'])
        
            if len(request.FILES) <= 0:
                member.image = 'usrImages/default.png'
            else:
                member.image = request.FILES['image']
            
            try: member.save()
            except IntegrityError: return HttpResponseBadRequest("Email already in use")

            member.save()
            
            return logIn(request) 
        else:
            return HttpResponseBadRequest("Invalid form!")

#called from login.html as post request, checks login credentials
#renders index for the time being
def logIn(request):
    if not ('email' in request.POST and 'password' in request.POST):
        return HttpResponseBadRequest("Invalid form!")
    else:        
        email = request.POST['email']
        password = request.POST['password']        
        try: 
            member = Member.objects.get(email=email)
        except Member.DoesNotExist: 
            return HttpResponseBadRequest('ERROR: No user found with email: ' + email)

        if member.check_password(password):
            request.session['email'] = email
            request.session['password'] = password
            member = Member.objects.get(email=email)

            #temporarily returns to index.html
            #response = render(request, 'movies/index.html', context)
            return index(request)

            now = datetime.datetime.utcnow()
            max_age = 24 * 60 * 60  #one day
            delta = now + datetime.timedelta(seconds=max_age)
            format = "%a, %d-%b-%Y %H:%M:%S GMT"
            expires = datetime.datetime.strftime(delta, format)
            response.set_cookie('last_login',now,expires=expires)
            
            return response
        else:
            return HttpResponseBadRequest('Wrong password')
                
    return index(request)

#flushes session 
def logOut(request):
    request.session.flush()
    return index(request)
    #return render(request, 'movies/index.html')

#if user is logged in return the user else return None
def getLoggedInUser(request):
    if 'email' in request.session:
        email = request.session['email']
        try: member = Member.objects.get(email=email)
        except Member.DoesNotExist: raise Http404('Member does not exist')
        return member
    else:
        return None

#End Refactored login
###########################################################################################
#page views
def index(request):
    context = {}

    #first check whether a user is logged in and set contexts
    loggedInUser = getLoggedInUser(request)
    if loggedInUser != None:
        context["user"] = loggedInUser
        context["LoggedIn"] = True
    else:
        context["user"] = None
        context["LoggedIn"] = False
    
    #this is between range of 1 inclusive and 251 exclusive (due to django 1 indexing)
    #will not have repeats
    randindexes = np.random.choice(np.arange(1,251), 5, replace=False)
    
    #get movie by index then get its similars, create a list to combine them into a row
    #append to movie rows
    #movie rows is a 2d list of movie objects
    movieRows = []
    for i in randindexes:
        movie = Movie.objects.get(id = i)
        similarMovies = movie.getSimilarMovies()
        simList = list(similarMovies)
        simList.insert(0,movie)
        movieRows.append(simList)

    context ["movieRows"] = movieRows
    return render(request, 'movies/index.html', context)


def moviePage(request, id):
    movie = Movie.objects.get(id = id)
    similarMovies = movie.getSimilarMovies()
    context = {
        "movie": movie,
        "similarMovieList": similarMovies,
        "reviews" : movie.reviews.all(),
    }

    loggedInUser = getLoggedInUser(request)
    if loggedInUser != None:
        context["user"] = loggedInUser
        context["LoggedIn"] = True
    else:
        context["user"] = None
        context["LoggedIn"] = False
    
    if request.method == 'POST':
        if loggedInUser != None:
            Review.objects.create(author = loggedInUser, text = request.POST['text'], movie = movie)
            reviews = movie.reviews.all()
            #as author is foreign key to reviews, needed to add natural foreign keys for serialisation
            data = serializers.serialize('json', reviews, use_natural_foreign_keys=True, use_natural_primary_keys=True)
            return JsonResponse(data=data, safe=False)
        else:
            return HttpResponseBadRequest('please Log In to submit a review')

    return render(request, 'movies/moviepage.html', context)

def testingExperiment(request):
    movieTestSet = [80, 138, 155, 176, 218, 129, 90, 207, 166, 76, 95, 203, 99, 105, 225, 246, 18, 158, 9, 56]
    context = {}
    
    loggedInUser = getLoggedInUser(request)
    if loggedInUser != None:
        context["user"] = loggedInUser
        context["LoggedIn"] = True
    else:
        return signIn(request)

        
    if request.method == 'GET':
        request.session['counter'] = 0
        count = request.session['counter']
        request.session['answers'] = []
    elif request.method == 'POST':
        if request.session['counter']  >= 19:
            print(request.session['answers'])
            ans = request.session['answers']
            #have to store array as a string because django does not have array fields for sqlite dbs
            stringAns = ";".join(ans)
            loggedInUser.answers = stringAns
            loggedInUser.save()
            request.session['answers'] = []
            return HttpResponse('Thank you for taking the time to complete this experiment!')
        
        request.session['counter'] += 1
        count = request.session['counter']
        answer = request.POST['choice']
        #append answer to the array
        if not 'answers' in request.session or not request.session['answers']:
            request.session['answers'] = [answer]
        else:
            answers_list = request.session['answers']
            answers_list.append(answer)
            request.session['answers'] = answers_list

    movie = Movie.objects.get(id = movieTestSet[count])
    similarMovies = movie.getSimilarMovies()
    randMoviesIndexes= np.random.choice(np.arange(1,251), 10, replace=False)
    randMovies = Movie.objects.filter(id__in=randMoviesIndexes)
    
    context["movie"] = movie
    context["similarMovieList"] = similarMovies
    context["randomMovieList" ] = randMovies

    return render(request, 'movies/test.html', context)
#########################################################################################