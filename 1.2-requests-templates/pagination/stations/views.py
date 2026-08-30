from csv import DictReader

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    page = int(request.GET.get('page', 1))

    with open(BUS_STATION_CSV, 'r', encoding='UTF-8') as csvfile:
        reader = DictReader(csvfile)
        lst = []
        for row in reader:
            lst.append(row)

        paginator = Paginator(lst, 10)
        page_obj = paginator.get_page(page)

    context = {
        'bus_stations': page_obj.object_list,
        'page': page_obj,
    }

    return render(request, 'stations/index.html', context)
