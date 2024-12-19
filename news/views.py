# news/views.py
from django.shortcuts import render
from news.services import get_news
from django.core.paginator import Paginator


def articles(request):
    # here pass location as url param
    location = 'London'  # Fetch location if provided
    news_data = get_news(location=location)  # Get news based on location

    if news_data:  # If data is available
        paginator = Paginator(news_data, 3)  # 3 news items per page
        page_number = request.GET.get('page')  # Get the page number from URL parameters
        page_obj = paginator.get_page(page_number)  # Get the news items for the current page
        return render(request, 'news/articles.html', {'page_obj': page_obj, 'location': location})
    else:  # If no news data available
        return render(request, 'news/articles.html', {'error': 'No news available', 'location': location})
