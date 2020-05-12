import json

from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from content.models import Content, Category, Images, Comment
from home.models import Setting, ContactFormu, ContactFormMessage
from home.forms import SearchForm, SignUpForm


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Content.objects.all()[:3]
    category = Category.objects.all()

    latestnews = Content.objects.raw(
        'SELECT content_content.* FROM content_content LEFT JOIN content_category ON content_content.category_id = content_category.id WHERE content_category.tree_id = 3')[
                 -3:]
    latestevents = Content.objects.raw(
        'SELECT content_content.* FROM content_content LEFT JOIN content_category ON content_content.category_id = content_category.id WHERE content_category.tree_id = 2')[
                   -3:]
    latestannouns = Content.objects.raw(
        'SELECT content_content.* FROM content_content LEFT JOIN content_category ON content_content.category_id = content_category.id WHERE content_category.tree_id = 1')[
                    -3:]

    # latestnews = Content.objects.filter(category_id=5).reverse()[:4]
    # newscontents = Content.objects.all().order_by('-id')[:4]
    # randomcontents = Content.objects.all().order_by('?')[:4]
    # form = SignUpForm()

    context = {'setting': setting,
               'page': 'home',
               'category': category,
               'sliderdata': sliderdata,
               'latestnews': latestnews,
               'latestevents': latestevents,
               'latestannouns': latestannouns
               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'hakkimizda', 'category': category}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'page': 'referanslar', 'category': category}
    return render(request, 'referanslarimiz.html', context)


def iletisim(request):
    if request.method == 'POST':  # form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir.Teşekkür Ederiz ")
            return HttpResponseRedirect('/iletisim')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactFormu()
    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'iletisim.html', context)


def categories(request, id, slug):
    # setting = Setting.objects.get(pk=1)
    try:
        category = Category.objects.all()
        categorydata = Category.objects.get(pk=id)
        contents = Content.objects.filter(category_id=id)
    except:
        return HttpResponseRedirect("/error")
    context = {'categories': categories,
               'category': category,
               'contents': contents,
               'categorydata': categorydata
               }
    return render(request, 'categories.html', context)


def content_detail(request, id, slug):
    # setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    try:
        content = Content.objects.get(pk=id)
        images = Images.objects.filter(content_id=id)
        comments = Comment.objects.filter(content_id=id, status='True')

        context = {
            'content': content, 'slug': slug, 'category': category, 'images': images, 'comments': comments,
        }
        return render(request, 'content_detail.html', context)
    except:
        messages.warning(request, "Hata ! İlgili içerik bulunamadı ")
    link = '/error'
    return HttpResponseRedirect(link)


def content_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                contents = Content.objects.filter(title__icontains=query)
            else:
                contents = Content.objects.filter(title__icontains=query, category_id=catid)

            context = {'contents': contents, 'category': category}

            return render(request, 'content_search.html', context)

        return HttpResponseRedirect('/')


def content_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        content = Content.objects.filter(title__icontains=q)
        results = []
        for rs in content:
            content_json = {}
            content_json = rs.title
            results.append(content_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası ! Kullanıcı adı veya şifre yanlış ")
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category}

    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category, 'form': form}
    return render(request, 'signup.html', context)


def error(request):
    category = Category.objects.all()

    setting = Setting.objects.get(pk=1)
    context = {
         'setting': setting, 'category': category,
    }
    return render(request, 'error_page.html', context)
