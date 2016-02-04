from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from pick.models import *
from mynewsite import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

#helper that gets the title of each link. adapted from https://docs.python.org/3.5/howto/urllib2.html
import json, urllib
import urllib.request
from http import client as Client

def getJSONResponse(l):
    key = '96cc6fb6ff8546c097d665078108b6af'
    fullLink = "http://api.embed.ly/1/oembed?key=:%s&url=%s&maxwidth=300"%(key, l)

    with urllib.request.urlopen(fullLink) as response:
        JSONMessage = response.read().decode()
    
    result = json.loads(JSONMessage)

    return result

def getTitle(link):
    dictionary = getJSONResponse(link)
    return dictionary["title"]

#adapted from http://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users
def get_all_logged_in_users():
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)

#adapted from http://www.djangobook.com/en/2.0/chapter14.html
def Register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/login/")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {'form': form,})

#adapted from Django Documentation on the authentication system
def Login(request):
    next = request.GET.get('next', '/')
    if request.method == "POST":
        data = dict(request.POST)
        username = data["username"][0]
        password = data["password"][0]
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, 'login.html', {"redirect_to": next})

#adapted from Django Documentation on the authentication system
def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

def Help(request):
    if request.method=="GET":
        context = {}
        username = "None"
        if request.user.is_authenticated():
            username = request.user.username
        else:
            username = ""
        context["username"] = " " + username
        return render(request, 'help.html', context)
    else:
        return HttpResponseRedirect('/help/')

@login_required
def Result(request):
    if request.method=="GET":
        context = {}
        all_options = Option.objects.all()
        for op in all_options:
            if op.isResult:
                context["result"] = op.optionContent
                return render(request, 'result.html', context)
        return Home(request)
    else:
        data = dict(request.POST)
        if "notResult" in data:
            option = Option.objects.get(optionContent=data["notResult"][0])
            option.isResult = False
            option.save()
            FinalVote.objects.all().delete()
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/result/')

@login_required
def Grid(request):
    if request.method=="GET":
        all_options = Option.objects.all()
        all_criteria = Criterion.objects.all()
        all_rates = Rate.objects.all()

        if all_rates == []:
            return render(request, 'gridview.html', {})

        options_data = [] 
        criteria_data = [] 
        users_data = [] 

        #get Criteria
        exist = []
        for criterion in all_criteria:
            if criterion.name not in exist:
                newCriterion = {}
                newCriterion["name"] = criterion.name
                newCriterion["weight"] = "*"*criterion.weight
                criteria_data.append(newCriterion)
                exist.append(criterion.name)

        #get users
        for rate in all_rates:
            if rate.ratername not in users_data:
                users_data.append(rate.ratername)

        #get ratings for each option
        for option in all_options:
            newOption = {}
            newOption["name"] = option.name
            newOption["content"] = option.optionContent
            newOption["users"] = []

            weightedAverage = 0
            divideBy = 0

            for user in users_data:
                userRating = []
                for criterion in criteria_data:
                    c = None
                    for x in all_criteria:
                        if x.name == criterion["name"] and x.option == option:
                            c = x
                    try:
                        rate = Rate.objects.get(option=option, criterion=c, ratername=user)
                        number = rate.number
                        userRating.append(str(number))
                        divideBy += c.weight
                        weightedAverage += number * c.weight
                    except:
                        userRating.append("-")
                if divideBy == 0:
                    newOption["weightedAverage"] = "0"
                else:
                    newOption["weightedAverage"] = str(round(weightedAverage/divideBy, 2))
                newOption["users"].append(userRating)
            if users_data == []:
                newOption["users"] = [["-"]]
            if weightedAverage == 0:
                newOption["weightedAverage"] = "0"
            options_data.append(newOption)

        #sort based on average
        options_data = reversed(sorted(options_data, key=lambda o_obj: o_obj["weightedAverage"]))    

        context = {}
        context["users_data"] = users_data
        context["options_data"] = options_data
        context["criteria_data"] = criteria_data
        context["numberOfUsersTimesNumberOfCriteria"] = str(len(users_data)*len(criteria_data))
        context["numberOfCriteria"] = str(len(criteria_data))


        #get username
        username = "None"
        if request.user.is_authenticated():
            username = request.user.username
        context["username"] = username

        return render(request, 'gridview.html', context)
    else:
        return HttpResponseRedirect('/gridview/')

@login_required
def Home(request):
    if request.method == "GET":
        context = {}

        all_options = Option.objects.all()
        all_criteria = Criterion.objects.all()
        all_pros = Pro.objects.all()
        all_cons = Con.objects.all()
        all_rates = Rate.objects.all()
        all_finalVotes = FinalVote.objects.all()
        goal = Goal.objects.all()

        options_data = [] #a list of dict
        criteria_data = [] #a list of dict

        #get goal
        try:
            context["goal_data"] = [goal[0].content]
        except:
            pass

        #get username
        username = "None"
        if request.user.is_authenticated():
            username = request.user.username
        context["username"] = username

        #get all logged-in users
        users = get_all_logged_in_users()
        usersStr = ""
        for u in users:
            if u != request.user:
                usersStr += ", " + u.username
        
        context["allLoggedInUsers"] = get_all_logged_in_users() #usersStr[2:]

        #get Criteria
        exist = []
        for criterion in all_criteria:
            if criterion.name not in exist:
                newCriterion = {}
                newCriterion["name"] = criterion.name
                newCriterion["weight"] = "*"*criterion.weight
                criteria_data.append(newCriterion)
                exist.append(criterion.name)

        #get Options
        for option in all_options:
            newOption = {}
            newOption["name"] = option.name
            newOption["optionContent"] = option.optionContent

            #add ratings for each criterion to each option
            newOption["criteria"] = []
            #each "ratings" item is a dictionary that contains ratings for 
                #each criterion and other relavent information after
                #some computation

            newOption["generalAverage"] = 0 #the average calculated with the consideration of different criterion's weight
            divideBy = 0
            usernames = [] #a list of usernames
            for criterion in all_criteria:
                if criterion.option == option:
                    criterionRatings = {}
                    criterionRatings["name"] = criterion.name
                    criterionRatings["weight"] = criterion.weight

                    #add Rates
                    criterionRatings["rates"] = []
                    totalRate = 0
                    numberOfRater = 0
                    for rate in all_rates:
                        if rate.option == option and rate.criterion == criterion:
                            newRate = {}
                            newRate["ratername"] = rate.ratername
                            newRate["number"] = rate.number
                            criterionRatings["rates"].append(newRate)
                            totalRate += rate.number
                            numberOfRater += 1
                            if rate.ratername not in usernames:
                                usernames.append(rate.ratername)
                    criterionRatings["numberOfRater"] = numberOfRater
                    criterionRatings["totalRate"] = totalRate
                    if numberOfRater != 0:
                        criterionRatings["averageRating"] = str(round(totalRate/numberOfRater, 2))
                        newOption["generalAverage"] += criterion.weight*totalRate
                        divideBy += numberOfRater*criterion.weight
                    else:
                        criterionRatings["averageRating"] = "0"
                    newOption["criteria"].append(criterionRatings)

            if divideBy != 0:
                newOption["generalAverage"] = str(round(newOption["generalAverage"]/divideBy, 2))
            else:
                newOption["generalAverage"] = "0"

            newOption["ratedBy"] = ""
            for name in usernames:
                newOption["ratedBy"] += name + ", "
            if newOption["ratedBy"] != "":
                newOption["ratedBy"] = "-- rated by " + newOption["ratedBy"][:-2]

            #add pros
            newOption["pros"] = []
            for pro in all_pros:
                if pro.option == option:
                    newOption["pros"].append(pro.procontent)

            #add cons 
            newOption["cons"] = []
            for con in all_cons:
                if con.option == option:
                    newOption["cons"].append(con.concontent)

            #add finalVotes
            newOption["finalVotes"] = []
            for finalVote in all_finalVotes:
                if finalVote.option == option:
                    newOption["finalVotes"].append(finalVote.ratername)

            options_data.append(newOption)


        #sort options
        options_data = reversed(sorted(options_data, key=lambda o_obj: o_obj["generalAverage"]))

        
        context["options_data"] = options_data
        context["criteria_data"] = criteria_data



        return render(request, 'homepage.html', context)

    else: #request.method == "POST"
        data = dict(request.POST)

        #need to check if options/criteria/pros/cons already exist!

        #update goal
        if "goal" in data:
            if data["goal"][0] != "":
                Goal.objects.all().delete()
                goal = Goal(content=data["goal"][0])
                goal.save()

        #add a new criterion
        if "newCriterion" in data:
            name = data["newCriterion"][0].replace(" ", "-")
            weight = data["newCriterionWeight"][0]
            if weight != "" and name != "" and weight.isdigit():
                if 1 <= int(weight) <= 5:
                    #check repitition
                    exist = False
                    existingCriteriaType = []
                    for criterion in Criterion.objects.all():
                        if criterion.name == name:
                            if criterion.weight == weight:
                                exist = True # complete repitition, don't do anything
                            else:
                                exist = None # needs to update weight 

                    if exist == None:
                        exist = False
                        for criterion in Criterion.objects.all():
                            if criterion.name == name:
                                criterion.delete()
                    if exist == False:
                        if name != "" and weight != "":
                            for option in Option.objects.all():
                                weight = int(weight)
                                newCriterion = Criterion(name=name, option=option, weight=weight)
                                newCriterion.save()


        #delete a certain criterion
        elif "criterionDelete" in data:
            for cri in Criterion.objects.all():
                if cri.name == data["criterionDelete"][0]:
                    cri.delete()

        #add a new option
        elif "newOptionContent" in data:
            optionContent = data["newOptionContent"][0]
            if optionContent != "":
                name = getTitle(optionContent)

                #check repitition
                exist = False
                for option in Option.objects.all():
                    if option.optionContent==optionContent or option.name==name:
                        exist = True
                if not exist:
                    newOption = Option(name=name, optionContent=optionContent)
                    newOption.save()

                    #add previous criteria
                    existingCriteriaType = []
                    for criterion in Criterion.objects.all():
                        if criterion.name not in existingCriteriaType:
                            newCriterion = Criterion(name=criterion.name, option=Option.objects.get(name=name))
                            newCriterion.save()
                            existingCriteriaType.append(criterion.name)

        elif "deleteOption" in data:
            option = Option.objects.get(optionContent=data["deleteOption"][0])
            option.delete()

        elif "reset" in data:
            Option.objects.all().delete()
            Criterion.objects.all().delete()
            Pro.objects.all().delete()
            Con.objects.all().delete()
            Rate.objects.all().delete()
            Goal.objects.all().delete()

        elif "newPro" in data:
            option = Option.objects.get(optionContent=data["proOption"][0])
            procontent = data["newPro"][0].replace(" ", "-")
            if procontent != "":

                #check repitition
                exist = False
                for pro in Pro.objects.all():
                    if pro.procontent==procontent and pro.option==option:
                        exist = True
                if not exist:
                    newPro = Pro(procontent=procontent, option=option)
                    newPro.save()

        elif "proDelete" in data:
            option = Option.objects.get(optionContent=data["proOption"][0])
            procontent = data["proDelete"][0]
            for pro in Pro.objects.all():
                if pro.procontent==procontent and pro.option==option:
                    pro.delete()

        elif "newCon" in data:
            option = Option.objects.get(optionContent=data["conOption"][0])
            concontent = data["newCon"][0].replace(" ", "-")
            if concontent != "":

                #check repitition
                exist = False
                for con in Con.objects.all():
                    if con.concontent==concontent and con.option==option:
                        exist = True
                if not exist:
                    newCon = Con(concontent=concontent, option=option)
                    newCon.save() 

        elif "conDelete" in data:
            option = Option.objects.get(optionContent=data["conOption"][0])
            concontent = data["conDelete"][0]
            for con in Con.objects.all():
                if con.concontent == concontent and con.option == option:
                    con.delete()

        elif "newRate" in data:
            number = data["newRate"][0]
            if number != "" and number.isdigit() and 1 <= int(number) <= 5:
                number = str(number)
                option = Option.objects.get(optionContent=data["rateOption"][0])
                criterion = None
                for c in Criterion.objects.all():
                    if c.name == data["rateCriterion"][0] and c.option == option:
                        criterion = c

                username = "None"
                if request.user.is_authenticated():
                    username = request.user.username

                exist = False
                for rate in Rate.objects.all():
                    if rate.ratername == username and rate.criterion == criterion and rate.option == option:
                        rate.number = number
                        exist = True
                        rate.save()
                if not exist:
                    newRate = Rate(ratername=username, criterion=criterion, option=option, number=number)
                    newRate.save()

        elif "result" in data:
            username = "None"
            if request.user.is_authenticated():
                username = request.user.username

            option = Option.objects.get(optionContent=data["result"][0])
            try: #check repitition
                f = FinalVote.objects.get(ratername=username, option=option)
            except:
                newFinalVote = FinalVote(ratername=username, option=option)
                newFinalVote.save()
            numOfUsers = len(get_all_logged_in_users())
            numOfFinalVoteForOption = 0
            for finalVote in FinalVote.objects.all():
                if finalVote.option == option:
                    numOfFinalVoteForOption += 1
            if numOfFinalVoteForOption >= numOfUsers:
                option.isResult = True
                option.save()
                return HttpResponseRedirect('/result/')

        elif "resetResult" in data:
            option = Option.objects.get(optionContent=data["resetResult"][0])
            for finalVote in FinalVote.objects.all():
                if finalVote.option == option:
                    finalVote.delete()

        return HttpResponseRedirect('/')






#below is some garbage that I threw out in the process of writing this app. 
#they are here just in case I need them in the future
'''
    if request.method == "GET":
        #get posts
        all_posts = Post.objects.all()
        posts_data = []
        for q in all_posts:
            q_obj = {}
            q_obj["content"] = q.content
            q_obj["name"] = q.name
            q_obj["pros"] = []
            q_obj["cons"] = []
            q_obj["rates"] = []

            all_pros = Pro.objects.all()
            for p in all_pros:
                if p.post == q:
                    q_obj["pros"].append(p.procontent)

            all_cons = Con.objects.all()
            for c in all_cons:
                if c.post == q:
                    q_obj["cons"].append(c.concontent)

            all_rates = Rate.objects.all()
            for r in all_rates:
                if r.post == q:
                    q_obj["rates"].append(r) #append the Rate object, not a string!

            q_obj["votedBy"] = str(q.votedBy)
            if q.votedBy == 0:
                q_obj["averagerating"] = "0"
            else:
                q_obj["averagerating"] = str(round(q.totalVotes/q.votedBy, 2))
            posts_data.append(q_obj)

        #sort the list
        posts_data = reversed(sorted(posts_data, key=lambda q_obj: q_obj["averagerating"]))

        #get goals
        all_goals = Goal.objects.all()
        goals_data = []
        for g in all_goals:
            g_obj = {}
            g_obj["gcontent"] = g.gcontent
            goals_data.append(g_obj)

        context = {}
        context["posts_data"] = posts_data
        context["goals_data"] = goals_data

        username = "None"
        if request.user.is_authenticated():
            username = request.user.username
        context["username"] = username

        return render(request, 'homepage.html', context)
    
    else: #is a POST!!!
        def existsAlready(t, content):
            if t == "Post":
                all_posts = Post.objects.all()
                for q in all_posts:
                    if q.content == content:
                        return True
            elif t == "Goal":
                all_goal = Goal.objects.all()
                for g in all_goal:
                    if content == g.gcontent:
                        return True
            return False

        data = dict(request.POST)

        if "p_content" in data:
            content = data["p_content"][0]
            name = data["p_name"][0]
            if content!= "" and name != "" and not existsAlready("Post", content):
                post_entry = Post(content=content, name=name)
                post_entry.save()

        elif "gcontent" in data:
            content = data["gcontent"][0].replace(" ", "-")
            if content != "" and not existsAlready("Goal", content):
                goal_entry = Goal(gcontent=content)
                goal_entry.save()

        elif "pdelete" in data:
            deleteContent = data["pdelete"][0]
            p = Post.objects.get(content=deleteContent)
            p.delete()

        elif "gdelete" in data:
            deleteContent = data["gdelete"][0]
            for g in Goal.objects.all():
                if "".join((g.gcontent).split(" ")) == deleteContent:
                    g.delete()
                    break

        elif "prodelete" in data:
            deletePro = data["prodelete"][0]
            propost = Post.objects.get(content=data["propost"][0])
            for p in Pro.objects.all():
                if p.procontent == deletePro and 1/0 and p.post == propost:
                    p.delete()
                    1/0
                    break

        elif "condelete" in data:
            deleteCon = data["condelete"][0]
            conpost = Post.objects.get(content=data["conpost"][0])
            for c in Con.objects.all():
                if c.concontent == deleteCon and c.post == conpost:
                    c.delete()
                    break

        elif "pro" in data:
            post_content = data["post_content"][0]
            post = Post.objects.get(content=post_content)
            procontent = data["pro"][0].replace(" ", "-")
            exist = False
            for p in Pro.objects.all():
                if p.procontent == procontent and post_content == p.post.content:
                    exist = True
            if exist == False and procontent!="":
                p_entry = Pro(procontent=procontent, post=post)
                p_entry.save()

        elif "con" in data:
            post_content = data["post_content"][0]
            post = Post.objects.get(content=post_content)
            concontent = data["con"][0].replace(" ", "-")
            exist = False
            for c in Con.objects.all():
                if c.concontent == concontent and post_content == c.post.content:
                    exist = True
            if exist == False and concontent!="":
                c_entry = Con(concontent=concontent, post=post)
                c_entry.save()

        elif "rate" in data:
            post_content = data["post"][0]
            votes = int(data["rate"][0])
            ratername = request.user.username
            post = Post.objects.get(content=post_content)
            exist = False
            for r in Rate.objects.all():
                #update rating by same user for same post
                if r.ratername == ratername and r.post == post: 
                    post.totalVotes -= r.votes
                    r.votes = votes
                    post.totalVotes += r.votes
                    exist = True
                    r.save()
                    post.save()
            if not exist:
                post.totalVotes += votes
                post.votedBy += 1
                post.save()
                newRate = Rate(ratername=ratername, votes=votes, post=post)
                newRate.save()

        elif "result" in data:
            post_content = data["result"][0]
            p = Post.objects.get(content=post_content)
            p.isResult = True
            p.save()
            return HttpResponseRedirect('/result/')

        elif "reset" in data:
            Post.objects.all().delete()
            Goal.objects.all().delete()
            Pro.objects.all().delete()
            Con.objects.all().delete()

        return HttpResponseRedirect('/')
'''