from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


from notifications.models import user_notifications

# Create your views here.
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





def get_user_obj(request):
    return User.objects.get(username=request.user.username)



def noti_count(request):
    user_obj=User.objects.get(username=request.user.username)
    noti_query=user_notifications.objects.filter(receiver=user_obj,read=False)
    noti_count=noti_query.count()

    print(noti_count)
    return JsonResponse({'noti_count': noti_count}, safe=False)



@login_required(login_url='/login')
def notifications(request):
    user_obj=get_user_obj(request)
    notifications=user_notifications.objects.filter(receiver=user_obj).order_by('-date')
    for x in notifications:
        x.pro=User.objects.get(username=x.sender)
    print(notifications)

    page = request.GET.get('page', 1)
    paginator = Paginator(notifications, 50)
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)

    user_notifications.objects.filter(receiver=user_obj,read=False).update(read=True)


    context={
        'notifications':notifications,
    }

    return render(request,'notifications.html',context)


