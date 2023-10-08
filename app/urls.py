from django.urls import path
from .views import home, stock_detail,download_queries,load_more_stocks

urlpatterns = [
    path('', home, name='home'),

    path('stock/<slug:slug>/', stock_detail, name='stock_detail'),
    path('download-queries/', download_queries, name='download_queries'),
    path('load-more-stocks/',load_more_stocks,name='load_more_stocks'),
]
