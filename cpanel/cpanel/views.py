from django.shortcuts import render
from django.contrib import auth
import pyrebase
config={
    
    'apiKey': "AIzaSyBRRbUKVoA5jbgEzkWJn_-0TYsIN7xpibo",
    'authDomain': "prison-54644.firebaseapp.com",
    'databaseURL': "https://prison-54644.firebaseio.com",
    'projectId': "prison-54644",
    'storageBucket': "prison-54644.appspot.com",
    'messagingSenderId': "697584156491",
   ' appId': "1:697584156491:web:a365e543b04d31ff89b2ce",
    'measurementId': "G-YG2Q5TV4N2"
}
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()

def signIn(request):
    return render(request,"signIn.html")

def postsign(request):
    email=request.POST.get('email')
    passw=request.POST.get("pass")
    try:
        user=authe.sign_in_with_email_and_password(email,passw)
    except:
        message="Invalid email or password"
        return render(request, "signIn.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"welcome.html",{"e":email})

def logout(request):
    auth.logout(request)
    return render(request, "signIn.html")

def signUp(request):
    return render(request, "signUp.html")
def postsignUp(request):
    name=request.POST.get('username')
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
        user=authe.create_user_with_email_and_password(email,password)
    except:
        message=("Please enter correct details.")
        return render(request,"signUp.html",{"message":message})
    uid=user['localId']
    data={"name":name,"status":"1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")
def Prisoners(request):
    return render(request,"prisoners.html")

def addPrisoner(request):
    return render(request,"addprisoner.html")

def postaddprisoner(request):

    import time
    from datetime import datetime,timezone
    import pytz

    tz=pytz.timezone('Asia/Kolkata')
    time_now=datetime.now(timezone.utc).astimezone(tz)
    millis=int(time.mktime(time_now.timetuple()))
    prisonerName=request.POST.get('name')
    prisonerID=request.POST.get('id')
    cellNo=request.POST.get('cellno')
    photo=request.POST.get('img1')
    fingerprint=request.POST.get('img2')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
    crimedetails=request.POST.get('details')
    arrival=request.POST.get('arrival')
    duration=request.POST.get('duration')
    url1=request.POST.get('url1')
    url2=request.POST.get('url2')
    idtoken=request.session['uid']
    a=authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    a=a['localId']
    data = {
        "prisonerName": prisonerName,
        "prisonerID": prisonerID,
        "cellNo": cellNo,
        "photo": photo,
        "fingerprint": fingerprint,
        "state": state,
        "pincode": pincode,
        "crimedetails": crimedetails,
        "arrival": arrival,
        "duration": duration,
        "photo": url1,
        "fingerprint":url2
        
    }
    database.child('users').child(a).child('info').child('prisoners').child(millis).set(data)

    return render(request,"prisoners.html")

def viewPrisoner(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timestamps=database.child("users").child(a).child('info').child('prisoners').shallow().get().val()

    lis_time=[]
    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    name=[]

    for i in lis_time:
        nam=database.child('users').child(a).child('info').child('prisoners').child(i).child('prisonerName').get().val()
        name.append(nam)
    date=[]
    for i in lis_time:
        i=float(i)
        dat=datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y')
        date.append(dat)

    comb_lis=zip(lis_time,date,name)


    return render(request,"viewprisoner.html",{'comb_lis':comb_lis})

def post_check(request):
    import datetime
    time=request.GET.get('z')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('info').child('prisoners').child(time).child('prisonerName').get().val()
    print(name)
    id = database.child('users').child(a).child('info').child('prisoners').child(time).child('prisonerID').get().val()
    cellNo = database.child('users').child(a).child('info').child('prisoners').child(time).child('cellNo').get().val()
    photo = database.child('users').child(a).child('info').child('prisoners').child(time).child('photo').get().val()
    fingerprint = database.child('users').child(a).child('info').child('prisoners').child(time).child('fingerprint').get().val()
    state = database.child('users').child(a).child('info').child('prisoners').child(time).child('state').get().val()
    pincode = database.child('users').child(a).child('info').child('prisoners').child(time).child('pincode').get().val()
    crimedetails = database.child('users').child(a).child('info').child('prisoners').child(time).child('crimedetails').get().val()
    arrival = database.child('users').child(a).child('info').child('prisoners').child(time).child('arrival').get().val()
    duration = database.child('users').child(a).child('info').child('prisoners').child(time).child('duration').get().val()

    return render(request,'post_check.html',{'name':name,'id':id,'cellNo':cellNo,'photo':photo,'fingerprint':fingerprint,'state':state,'pincode':pincode,'crimedetails':crimedetails,'arrival':arrival,'duration':duration})

def Guards(request):
    return render(request,"guards.html")

def addGuard(request):
    return render(request,"addGuard.html")

def postaddguard(request):

    import time
    from datetime import datetime,timezone
    import pytz

    tz=pytz.timezone('Asia/Kolkata')
    time_now=datetime.now(timezone.utc).astimezone(tz)
    millis=int(time.mktime(time_now.timetuple()))
    name=request.POST.get('name')
    guardID=request.POST.get('id')
    block=request.POST.get('block')
    photo=request.POST.get('img3')
    gender=request.POST.get('gender')
    address=request.POST.get('address')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
    url3=request.POST.get('url3')
    idtoken=request.session['uid']
    a=authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    a=a['localId']
    data = {
        "Name": name,
        "guardID": guardID,
        "block": block,
        "photo": photo,
        "gender": gender,
        "address": address,
        "state": state,
        "pincode": pincode,
        "photo": url3
        
    }
    database.child('users').child(a).child('info').child('guards').child(millis).set(data)
   

    return render(request,"guards.html", )

def viewGuards(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timestamps=database.child("users").child(a).child('info').child('guards').shallow().get().val()

    lis_time=[]
    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    name=[]

    for i in lis_time:
        nam=database.child('users').child(a).child('info').child('guards').child(i).child('Name').get().val()
        print(nam)
        name.append(nam)
    date=[]
    for i in lis_time:
        i=float(i)
        dat=datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y')
        date.append(dat)

    comb_lis=zip(lis_time,date,name)

    return render(request,"viewGuards.html",{'comb_lis':comb_lis})

def post_check2(request):
    import datetime
    time=request.GET.get('z')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('info').child('guards').child(time).child('Name').get().val()
    print(name)
    id = database.child('users').child(a).child('info').child('guards').child(time).child('guardID').get().val()
    block = database.child('users').child(a).child('info').child('guards').child(time).child('block').get().val()
    photo = database.child('users').child(a).child('info').child('guards').child(time).child('photo').get().val()
    gender = database.child('users').child(a).child('info').child('guards').child(time).child('gender').get().val()
    address = database.child('users').child(a).child('info').child('guards').child(time).child('address').get().val()
    state = database.child('users').child(a).child('info').child('guards').child(time).child('state').get().val()
    pincode = database.child('users').child(a).child('info').child('guards').child(time).child('pincode').get().val()

    return render(request,'post_check2.html',{'name':name,'id':id,'block':block,'photo':photo,'gender':gender,'address':address,'state':state,'pincode':pincode})


def postaddvisitor(request):
    import time
    from datetime import datetime,timezone
    import pytz

    tz=pytz.timezone('Asia/Kolkata')
    time_now=datetime.now(timezone.utc).astimezone(tz)
    millis=int(time.mktime(time_now.timetuple()))
    name=request.POST.get('vname')
    photo=request.POST.get('img4')
    gender=request.POST.get('gender')
    prisonerID=request.POST.get('id')
    address=request.POST.get('address')
    state=request.POST.get('state')
    pincode=request.POST.get('pincode')
    url4=request.POST.get('url4')
    idtoken=request.session['uid']
    a=authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    a=a['localId']
    data = {
        "Name": name,
        "photo": photo,
        "gender": gender,
        "prisonerID": prisonerID,
        "address": address,
        "state": state,
        "pincode": pincode,
        "photo": url4

    }
    database.child('users').child(a).child('info').child('visitors').child(millis).set(data)

    return render(request,"signIn.html", )


def viewVisitors(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timestamps=database.child("users").child(a).child('info').child('visitors').shallow().get().val()

    lis_time=[]
    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    name=[]

    for i in lis_time:
        nam=database.child('users').child(a).child('info').child('visitors').child(i).child('Name').get().val()
        print(nam)
        name.append(nam)
    date=[]
    for i in lis_time:
        i=float(i)
        dat=datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%y')
        date.append(dat)

    comb_lis=zip(lis_time,date,name)

    
    return render(request,"viewVisitors.html",{'comb_lis':comb_lis})

def post_check3(request):
    import datetime
    time=request.GET.get('z')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('info').child('visitors').child(time).child('Name').get().val()
    print(name)
    photo = database.child('users').child(a).child('info').child('visitors').child(time).child('photo').get().val()
    id = database.child('users').child(a).child('info').child('visitors').child(time).child('prisonerID').get().val()
    gender = database.child('users').child(a).child('info').child('visitors').child(time).child('gender').get().val()
    address = database.child('users').child(a).child('info').child('visitors').child(time).child('address').get().val()
    state = database.child('users').child(a).child('info').child('visitors').child(time).child('state').get().val()
    pincode = database.child('users').child(a).child('info').child('visitors').child(time).child('pincode').get().val()

    return render(request,'post_check3.html',{'name':name,'photo':photo,'id':id,'gender':gender,'address':address,'state':state,'pincode':pincode})