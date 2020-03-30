from django.shortcuts import render
from django.contrib import auth
import pyrebase
config={
    'apiKey': "AIzaSyCLjLncnTczSOD7yJd-mgSZLPoLl8icUZw",
    'authDomain': "cpanel-dee36.firebaseapp.com",
    'databaseURL': "https://cpanel-dee36.firebaseio.com",
    'projectId': "cpanel-dee36",
    'storageBucket': "cpanel-dee36.appspot.com",
    'messagingSenderId': "327800301185",
    'appId': "1:327800301185:web:a88b58fd51d71552f80f80",
    'measurementId': "G-S52R4GBPVW"
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
    database.child('users').child(a).child('info').child(millis).set(data)
    name=database.child('users').child(a).child('details').child('name').get().val()

    return render(request,"prisoners.html", {'e':name})

def viewPrisoner(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    timestamps=database.child("users").child(a).child('info').shallow().get().val()

    lis_time=[]
    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)
    name=[]

    for i in lis_time:
        nam=database.child('users').child(a).child('info').child(i).child('prisonerName').get().val()
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
    name = database.child('users').child(a).child('info').child(time).child('prisonerName').get().val()
    print(name)
    id = database.child('users').child(a).child('info').child(time).child('prisonerID').get().val()
    cellNo = database.child('users').child(a).child('info').child(time).child('cellNo').get().val()
    photo = database.child('users').child(a).child('info').child(time).child('photo').get().val()
    fingerprint = database.child('users').child(a).child('info').child(time).child('fingerprint').get().val()
    state = database.child('users').child(a).child('info').child(time).child('state').get().val()
    pincode = database.child('users').child(a).child('info').child(time).child('pincode').get().val()
    crimedetails = database.child('users').child(a).child('info').child(time).child('crimedetails').get().val()
    arrival = database.child('users').child(a).child('info').child(time).child('arrival').get().val()
    duration = database.child('users').child(a).child('info').child(time).child('duration').get().val()

    return render(request,'post_check.html',{'name':name,'id':id,'cellNo':cellNo,'photo':photo,'fingerprint':fingerprint,'state':state,'pincode':pincode,'crimedetails':crimedetails,'arrival':arrival,'duration':duration})

def Guards(request):
    return render(request,"guards.html")

def addGuard(request):
    return render(request,"addGuard.html")