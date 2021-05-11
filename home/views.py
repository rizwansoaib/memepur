from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.template.defaultfilters import slugify
from .models import *
from taggit.models import Tag
from django.contrib.auth.models import User
from notifications.models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.views.decorators.http import require_GET




from django.db.models import F

import simplejson as json
# Create your views here.




def robots(request):
    lines = [
        "User-Agent: *",
        "Allow: /",
        "Sitemap: http://memepur.in/sitemap.xml",

    ]


    return HttpResponse("\n".join(lines),content_type="text/plain")




def like_meme_message(sender,photo_id):
    msg=sender+' liked your memes'
    url='/post?id='+photo_id
    return msg,url
def comment_meme_message(sender,photo_id):
    msg=sender+' commented on your memes'
    url='/post?id='+photo_id
    return msg,url
def also_comment_message(sender,photo_id):
    msg=sender+'also commented on memes'
    url='/post?id='+photo_id
    return msg,url
def like_comment_message(sender,photo_id):
    url='/post?id='+str(photo_id.photo_id)
    msg=sender+' liked your comment'
    return msg,url



def get_photo_obj(photo_id):
    return photo.objects.get(photo_id=photo_id)

def get_comment_obj(comment_id):
    return user_comments.objects.get(comment_id=comment_id)

def get_user_obj(request):
    return User.objects.get(username=request.user.username)

def get_user_obj_name(username):
    return User.objects.get(username=username)

def is_like(self,request):
    user_obj=get_user_obj(request)
    return user_likes_photo.objects.filter(photo_id=self, username=user_obj).count()==1

def is_like_comment(self,request):
    user_obj=get_user_obj(request)
    return user_likes_comment.objects.filter(comment_id=self, username=user_obj).count()==1








def index(request):
    query = photo.objects.order_by('-view_count')

    if not request.user.is_authenticated:
        trending_list = {}
        for x in query:
            trending_list[x] = 2 * x.count_likes() + x.count_comments() + x.view_count // 1.3
        final_trending_dic = {k: v for k, v in sorted(trending_list.items(), key=lambda item: item[1], reverse=True)}
        final_trending = [x for x in final_trending_dic.keys()]
        print(final_trending_dic)
        # print(type(query))

        query=final_trending_dic

    else:

        rec_data=recommender.objects.annotate(recommend_score=F('view_count') + F('like_count')+ 2*F('comment_count')).order_by('-recommend_score')
        print(rec_data.values())

        query=set()
        for x in rec_data:
            tag = get_object_or_404(Tag, slug=x.tag)
            posts = photo.objects.filter(tags__in=[tag])
            query.update(posts)
        print('recommended post',query)
        following_list=follow.objects.filter(username=request.user.username)
        print(following_list)
        for x in following_list:
            post=photo.objects.filter(uploader=x.follow)
            query.update(post)
        print(query)
        posts = photo.objects.order_by('-date_time','-view_count')
        query.update(posts)
        print(query)


        for x in query:

            x.liked = is_like(x, request)
            #print(x)
            #print(x.view_count)

    page = request.GET.get('page', 1)
    paginator = Paginator(list(query), 20)
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)

    print(query)



    #print(numbers)
    context = {
        'post': query,
        #'numbers': numbers,
    }
    return render(request,'index.html',context)

def trending(request):
    query = photo.objects.order_by('-date_time','-view_count')
    if query.count()>100:
        query=query[:100]

    trending_list={}
    for x in query:
        trending_list[x]=2*x.count_likes()+x.count_comments() +x.view_count//4
    final_trending_dic={k: v for k, v in sorted(trending_list.items(), key=lambda item: item[1], reverse=True)}
    final_trending=[x for x in final_trending_dic.keys()]
    print(final_trending_dic)


    if request.user.is_authenticated:
        for x in query:
            x.liked = is_like(x, request)
            # print(x.liked)

    page = request.GET.get('page', 1)
    paginator = Paginator(final_trending, 20)
    try:
        final_trending = paginator.page(page)
    except PageNotAnInteger:
        final_trending = paginator.page(1)
    except EmptyPage:
        final_trending = paginator.page(paginator.num_pages)

    context = {
        'post': final_trending
    }
    return render(request,'index.html',context)

def recent(request):
    query = photo.objects.order_by('-date_time')
    # print(type(query))

    if request.user.is_authenticated:
        for x in query:
            x.liked = is_like(x, request)
            # print(x.liked)

    page = request.GET.get('page', 1)
    paginator = Paginator(query, 20)
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)

    context = {
        'post': query
    }
    return render(request,'index.html',context)



@login_required(login_url='/login')
def upload(request):
    if request.method=='POST':
        uploaded_file = request.FILES['photo']
        title=request.POST['title']
        tags=request.POST['tags']
        taglist = [str(slugify(r)) for r in tags.split('#')]
        tags=[]
        for r in taglist:
            if r:
                tags.append('#'+r)
        uploader = get_user_obj(request)

        row=photo.objects.create(url=uploaded_file,title=title,uploader=uploader)
        row.slug=tags
        row.tags.add(*tags)
        row.save()


    return  render(request,'upload.html')




def tag(request,tag_slug=None):
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        posts=photo.objects.filter(tags__in=[tag])

        for x in posts:
            x.pro = User.objects.get(username=x.uploader)

        if request.user.is_authenticated:

            exist_data=recommender.objects.filter(username=get_user_obj(request),tag=slugify(tag_slug)).first()
            print(exist_data)
            if exist_data:
                exist_data.view_count+=3
                exist_data.save()
            else:
                new=recommender(username=get_user_obj(request), tag=slugify(tag_slug),view_count=3)
                new.save()


            for x in posts:
                x.liked = is_like(x, request)
                #print(x.liked)

        context = {
            'post': posts,
        }

        #print(context)

        return render(request, 'index.html', context)


def autocomplete(request):
    term=request.GET.get('term',None)
    if term is not None:
        if '#' not in term:
            term='#'+term

        qs = Tag.objects.all()
        qs = qs.filter(name__icontains=request.GET.get('term'))
        titles = list()
        for search in qs:
            #print(search)
            titles.append(search.name)
        return JsonResponse(titles, safe=False)


def likepost(request):
    photo_id=request.GET.get('photo_id',None)
    if photo_id is not None:
        photo_obj=get_photo_obj(photo_id)
        user_obj=get_user_obj(request)
        photo_tags = photo_obj.tags.all()

        exist_data=user_likes_photo.objects.filter(photo_id=photo_obj,username=user_obj)
        if exist_data:
            exist_data.delete()

        else:
            row=user_likes_photo(username=user_obj,photo_id=photo_obj)
            row.save()
            for tag_slug in photo_tags:

                rec_exist_data = recommender.objects.filter(username=user_obj, tag=slugify(tag_slug)).first()
                if rec_exist_data:
                    rec_exist_data.like_count+=1
                    rec_exist_data.save()
                else:
                    new=recommender(username=user_obj, tag=slugify(tag_slug),like_count=1)
                    new.save()

            msg,url=like_meme_message(user_obj.username,photo_id)
            if not user_notifications.objects.filter(sender=user_obj,receiver=photo_obj.uploader,message=msg,type='2',url=url).count() and str(user_obj)!=str(photo_obj.uploader):
                row=user_notifications(sender=user_obj,receiver=photo_obj.uploader,message=msg,type='2',url=url)
                row.save()

            return JsonResponse({'status':'success'}, safe=False)
        return JsonResponse({'status': 'success'}, safe=False)
    return JsonResponse({'status': 'fail'}, safe=False)







def post(request):
    if request.method=='POST':
        photo_id=request.GET.get('id',None)
        data = request.POST['data']
        #print(photo_id,data)
        if photo_id and data:
            photo_obj=get_photo_obj(photo_id)
            photo_tags = photo_obj.tags.all()
            for tag_slug in photo_tags:
                print(slugify(tag_slug))

                exist_data = recommender.objects.filter(username=get_user_obj(request), tag=slugify(tag_slug)).first()
                if exist_data:
                    exist_data.comment_count += 1
                    exist_data.save()
                else:
                    new = recommender(username=get_user_obj(request), tag=slugify(tag_slug), comment_count=1)
                    new.save()


            user_obj=get_user_obj(request)
            #print(photo_obj,user_obj)
            row=user_comments(photo_id=photo_obj,username=user_obj,data=data)
            row.save()

            msg, url = comment_meme_message(user_obj.username, photo_id)
            if not user_notifications.objects.filter(sender=user_obj, receiver=photo_obj.uploader, message=msg,type='3', url=url).count() and str(user_obj)!=str(photo_obj.uploader):
                row = user_notifications(sender=user_obj, receiver=photo_obj.uploader, message=msg, type='3', url=url)
                row.save()


    id=request.GET.get('id',None)
    if id is not None:
        posts = photo.objects.get(photo_id=id)
        posts.view_count+=1
        print(posts.view_count)
        posts.save()
        photo_tags=posts.tags.all()



        photo_obj = get_photo_obj(id)
        comments=user_comments.objects.filter(photo_id=photo_obj)
        #print(comments)



        if request.user.is_authenticated:
            for tag_slug in photo_tags:
                print(slugify(tag_slug))

                exist_data = recommender.objects.filter(username=get_user_obj(request), tag=slugify(tag_slug)).first()
                print(exist_data)
                if exist_data:
                    exist_data.view_count += 1
                    exist_data.save()
                else:
                    new = recommender(username=get_user_obj(request), tag=slugify(tag_slug), view_count=1)
                    new.save()

            posts.liked = is_like(posts, request)
                #print(x.liked)
            for x in comments:
                x.liked = is_like_comment(x,request)

        context = {
            'x': posts,
            'comments':comments,
        }

        #print(context)

        return render(request, 'post.html', context)


def delete_comment(request):
    comment_id=request.GET.get('comment_id',None)
    if comment_id is not None:
        user_obj=get_user_obj(request)
        exist_data=user_comments.objects.get(comment_id=comment_id,username=user_obj)
        if exist_data:
            exist_data.delete()
            return JsonResponse({'status': 'success'}, safe=False)
    return JsonResponse({'status': 'fail'}, safe=False)




def likecomment(request):
    #print("enter in likecomment")
    comment_id=request.GET.get('comment_id',None)
    if comment_id is not None:
        comment_obj=get_comment_obj(comment_id)
        user_obj=get_user_obj(request)
        #print(comment_id,comment_obj,user_obj)
        exist_data=user_likes_comment.objects.filter(comment_id=comment_obj,username=user_obj)
        if exist_data.exists():
            exist_data.delete()
        else:
            row=user_likes_comment(comment_id=comment_obj,username=user_obj)
            row.save()

            photo_id=comment_obj.photo_id
            photo_obj=photo.objects.get(photo_id=photo_id)

            rec=user_comments.objects.get(comment_id=comment_obj)
            data_comments=rec.data
            print(data_comments)
            receiver=User.objects.get(username=rec.username)


            msg, url = like_comment_message(user_obj.username, photo_id)
            msg+=' '+data_comments
            print(user_obj,receiver)
            if not user_notifications.objects.filter(sender=user_obj, receiver=receiver, message=msg,type='5', url=url).count() and str(user_obj)!=str(receiver):
                row = user_notifications(sender=user_obj, receiver=receiver, message=msg, type='5', url=url)
                row.save()

            return JsonResponse({'status':'success'}, safe=False)
        return JsonResponse({'status': 'success'}, safe=False)
    return JsonResponse({'status': 'fail'}, safe=False)



def delete_post(request):
    photo_id=request.GET.get('photo_id',None)
    if photo_id is not None:
        user_obj=get_user_obj(request)
        exist_data=photo.objects.get(photo_id=photo_id,uploader=user_obj)
        if exist_data.exists():
            exist_data.delete()
            return JsonResponse({'status': 'success'}, safe=False)
    return JsonResponse({'status': 'fail'}, safe=False)
