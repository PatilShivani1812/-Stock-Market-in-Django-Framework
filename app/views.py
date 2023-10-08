from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Stock, Query
from .forms import QueryForm
from django.utils.text import slugify
import pandas as pd
from django.http import HttpResponse
from django.db.models import Q

def home(request):
    stocks = Stock.objects.all()
    return render(request, 'home.html', {'stocks': stocks})


@login_required
def stock_detail(request, slug):
    stock = Stock.objects.get(slug=slug)
    form = QueryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        query = form.save(commit=False)
        query.user = request.user
        query.stock = stock
        query.save()
        return redirect('home')

    return render(request, 'stock_detail.html', {'stock': stock, 'form': form})


@login_required
def download_queries(request):
    # Get queries for the logged-in user
    queries = Query.objects.filter(user=request.user)

    # Create a DataFrame from the Query objects
    data = {'User': [], 'Stock': [], 'Query Text': []}
    for query in queries:
        data['User'].append(str(query.user))
        data['Stock'].append(str(query.stock))
        data['Query Text'].append(query.query_text)

    df = pd.DataFrame(data)

    # Create a unique filename based on the user and timestamp
    filename = f"{slugify(request.user.username)}_queries.xlsx"

    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)

    # Create an HttpResponse with the Excel file for download
    with open(filename, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


# def load_more_stocks(request):
#     # Get parameters from the request, like the number of stocks to load, the current offset, and the search query
#     num_to_load = int(request.GET.get('num_to_load', 2))
#     offset = int(request.GET.get('offset', 0))
#     search_query = request.GET.get('search_query', '')

#     # If a search query is provided, filter stocks based on the query
#     if search_query:
#         stocks = Stock.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))[offset:offset + num_to_load]
#     else:
#         # If no search query, load more stocks without filtering
#         stocks = Stock.objects.all()[offset:offset + num_to_load]

#     # Convert stock data to a format suitable for JSON serialization
#     stock_data = [{'name': stock.name, 'description': stock.description, 'video_url': stock.video_url, 'slug': stock.slug} for stock in stocks]

#     # Create a JSON response
#     response_data = {'stocks': stock_data}

#     return JsonResponse(response_data)

from django.shortcuts import render
from django.db.models import Q
from .models import Stock

def load_more_stocks(request):
    # Get parameters from the request, like the number of stocks to load, the current offset, and the search query
    num_to_load = int(request.GET.get('num_to_load', 2))
    offset = int(request.GET.get('offset', 0))
    search_query = request.GET.get('search_query', '')

    # If a search query is provided, filter stocks based on the query
    if search_query:
        stocks = Stock.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))[offset:offset + num_to_load]
    else:
        # If no search query, load more stocks without filtering
        stocks = Stock.objects.all()[offset:offset + num_to_load]

    # Render an HTML template with the list of stocks
    return render(request, 'load_more_stocks.html', {'stocks': stocks})
