import allauth.account.views
from django.shortcuts import render
from home.models import *
from django.contrib.auth.models import User

from notifications.models import *

from login.models import *

from django.http import JsonResponse


# Create your views here.

from allauth.account.views import logout


def follow_message(sender):
    msg=sender+' started following you'
    url='/profile/?username='+sender
    return msg,url


def login(request):
    return render(request,'login.html')

def get_user_obj(username):
    try:
        return User.objects.get(username=username)
    except:
        return False



def already_following(request,username):
    user_obj=User.objects.get(username=username)

    return request.user.is_authenticated and follow.objects.filter(username=request.user.username,follow=user_obj).count()==1


def profile(request):
    username=request.GET.get('username',None)
    if username:
        user_obj=get_user_obj(username)
        if not user_obj:
            return render(request,'404.html')
        #print(user_obj)
        following_count=follow.objects.filter(username=username).count()
        follower_count=follow.objects.filter(follow=user_obj).count()
        afollow=already_following(request,username)
        liked_count=user_likes_photo.objects.filter(username=User.objects.get(username=username)).count()



        posts_count=photo.objects.filter(uploader=user_obj).count()

        context={
            'username':username,
            'posts_count':posts_count,
            'liked_count':liked_count,
            'follower_count':follower_count,
            'following_count':following_count,
            'afollow':afollow,
            'pro':user_obj,

        }




    return render(request,'profile.html',context)



def followurl(request):
    username=request.GET.get('username',None)
    if username is not None and request.user.is_authenticated:
        user_obj=get_user_obj(username)
        exist_data= follow.objects.filter(username=request.user.username,follow=user_obj)
        if exist_data:
            exist_data.delete()
        else:
            row=follow(username=request.user.username,follow=user_obj)
            row.save()
            msg, url = follow_message(request.user.username)
            print('noti start',msg,url)
            sender_obj=User(username=request.user.username)
            receiver_obj=user_obj
            if not user_notifications.objects.filter(sender=sender_obj, receiver=receiver_obj, message=msg,type='1', url=url).count():
                row = user_notifications(sender=sender_obj, receiver=receiver_obj, message=msg, type='1', url=url)
                row.save()
            return JsonResponse({'status': 'success'}, safe=False)
    return JsonResponse({'status': 'fail'}, safe=False)


def pro_liked(request):
    username = request.GET.get('username', None)
    if username is not None:
        user_obj = get_user_obj(username)
        if not user_obj:
            return render(request,'404.html')

        like_post=user_likes_photo.objects.filter(username=user_obj)

        posts=[]

        for x in like_post:
            posts.append(x.get_post())

        context={

            'like_post':True,

            'lposts':posts,
        }

    return render(request,'pro_post.html',context)




def follower_list(request):
    username=request.GET.get('username',None)
    if username is not None:
        user_obj = get_user_obj(username)
        if not user_obj:
            return render(request, '404.html')
        follower_list = follow.objects.filter(follow=user_obj)

        for x in follower_list:
            x.pro=get_user_obj(x.username)
            if request.user.is_authenticated:
                if follow.objects.filter(username=request.user.username,follow=User.objects.get(username=x.username)):
                    x.afollow=True
                else:
                    x.afollow=False


        context={
            'follower_list':follower_list,
        }
    return render(request,'followers.html',context)



def following_list(request):
    username=request.GET.get('username',None)
    if username is not None:
        user_obj = get_user_obj(username)
        if not user_obj:
            return render(request, '404.html')
        following_list = follow.objects.filter(username=username)

        for x in following_list:
            x.pro=User.objects.get(username=x.follow)
            if request.user.is_authenticated:
                if follow.objects.filter(username=request.user.username,follow=User.objects.get(username=x.follow)):
                    x.afollow=True
                else:
                    x.afollow=False
            x.username,x.follow=x.follow.username,User.objects.get(username=x.username)


        context={
            'follower_list':following_list,
        }
    return render(request,'followers.html',context)



def pro_post(request):
    username=request.GET.get('username',None)
    if username:
        user_obj=get_user_obj(username)
        if not user_obj:
            return render(request,'404.html')
        #print(user_obj)


        posts=photo.objects.filter(uploader=user_obj)

        context={
            'memes':True,
            'posts':posts,

        }




    return render(request,'pro_post.html',context)



def logout(request):
    return allauth.account.views.LogoutView()




def privacy(request):
    return render(request,'privacy.html')


def error404(request, exception):
    return render(request,'404.html')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        if name and email and message:
            row=contactus(name=name,email=email,message=message)
            row.save()
            context={
                'success':True,
                'name':name
            }
            return render(request, 'contact.html',context)
    return render(request,'contact.html')