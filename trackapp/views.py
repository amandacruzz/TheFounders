from django.shortcuts import render, redirect
from .models import *
from .forms import Lost_Item_Form
from plots.views import pieChart, linechartPlain, historicPriceChange, aggPos, getPrices
from plots.views import dashplotval
from django.core.files.storage import FileSystemStorage
# Create your views here.


def index(request):
    total_all_positions = lostItem.objects.count()
    user_count = User.objects.count()
    context = {
        'total_all_positions': total_all_positions,
        'user_count': user_count,
    }
    return render(request, 'index.html', context)


def donate(request):
    return render(request, 'donate.html')


def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')

def dashboard(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('/account/login/')
    #
    # prices = getPrices()
    # agg = aggPos(request.user)
    # stats = historicPriceChange(request)
    #
    # oneday = stats[0]
    # sevendays = stats[1]
    # fifteendays = stats[2]
    # thirtydays = stats[3]
    # sixtydays = stats[4]
    #
    # for i in prices:
    #     for j in agg:
    #         if i['symbol'] == j['ticker']:
    #             j['curPrice'] = i['derivedUSD']
    #             j['curValue'] = round(float(j['curPrice']) * j['quantity'], 2)
    #
    #             if j['cost'] == 0:
    #                 percent = (float(j['curPrice']) * j['quantity']) / (.00000001 * j['quantity'])
    #             else:
    #                 percent = (float(j['curPrice']) * j['quantity']) / (j['cost'] * j['quantity'])
    #
    #             if percent > 1:
    #                 percent = percent - 1
    #                 j['percent'] = str(round(percent * 100, 2))
    #             else:
    #                 percent = 1 - percent
    #                 j['percent'] = '-' + str(round(percent * 100, 2))

    context = {
        "prices": [],
        "aggregate_positions": [],
        'chart': "",
        'piechart': "",
        'portval': "",
        'oneday': 0.0,
        'sevendays': 0.0,
        'fifteendays': 0.0,
        'thirtydays': 0.0,
        'sixtydays': 0.0,
        "all_lost_found": lostItem.objects.all()
    }

    return render(request, 'dashboard.html', context)


def positions(request):
    if str(request.user) == 'AnonymousUser':
        return redirect('/account/login/')

    form = Lost_Item_Form(request.POST, request.FILES)

    if form.data:
        print(form.errors)
        print(request.FILES)
        position = form.save(commit=False)

        position.username_id = request.user

        position.save()

    user_lost_found = lostItem.objects.filter(username_id__username=request.user)

    total_all_positions = Acc_Positions.objects.count()
    user_positions = Acc_Positions.objects.filter(username_id__username=request.user)

    aggregate_pos = aggPos(request.user)

    total_positions = user_positions.count()
    context = {
        'total_positions': total_positions,
        'user_positions': user_positions,
        'total_all_positions': total_all_positions,
        'aggregate_positions': aggregate_pos,
        'form': form,
        "user_lost_found": user_lost_found
    }

    return render(request, 'positions.html', context)


def deletePosition(request, pk):
    position = lostItem.objects.get(id=pk)
    position.delete()
    return redirect('positions')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def notcreated(request):
    return render(request, 'notcreated.html')


def preview(request):
    return render(request, 'preview.html')


def faqs(request):
    return render(request, 'faqs.html')


def sponsor(request):
    return render(request, 'sponsor.html')

