from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from content.models import Content, Category, Images, Comment
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Content.objects.all()[:4]
    category = Category.objects.all()
    latestcontents = Content.objects.all()[:4]
    newscontents = Content.objects.all().order_by('-id')[:4]
    randomcontents = Content.objects.all().order_by('?')[:4]

    context = {'setting': setting,
               'page': 'home',
               'category': category,
               'sliderdata': sliderdata,
               'latestcontents': latestcontents,
               'newscontents': newscontents,
               'randomcontents': randomcontents
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
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    contents = Content.objects.filter(category_id=id)

    context = {'categories': categories,
               'category': category,
               'contents': contents,
               'categorydata': categorydata
               }
    return render(request, 'categories.html', context)


def content_detail(request, id, slug):
    # setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    content = Content.objects.get(pk=id)
    images = Images.objects.filter(content_id=id)
    comments = Comment.objects.filter(content_id=id, status='True')

    context = {
        'content': content, 'slug': slug, 'category': category, 'images': images, 'comments': comments,
    }
    return render(request, 'content_detail.html', context)
