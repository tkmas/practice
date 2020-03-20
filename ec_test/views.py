from django.shortcuts import render
from .models import ItemImage, Customer
from .forms import CustomerResisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def top_page(request):
    items = ItemImage.objects.all()
    return render(request, 'top.html',
                  {'items': items})


def item_detail(request, pk):
    item = ItemImage.objects.get(pk=pk)
    return render(request, 'detail.html',
                  {'item': item})


def log_in_page(request):
    return render(request, 'log-in.html')


def resister_user(request):
    form = CustomerResisterForm(request.POST or None)  # POSTがなければformをそのまま
    if form.is_valid():
        message = 'データの検証に成功しました'
    else:
        message = 'データの検証に失敗しました'

    if request.method == 'POST':
        return render(request, 'resister-user.html',
                      {'form': form, 'message': message})

    else:
        return render(request, 'resister-user.html',
                      {'form': form, 'message': message})
