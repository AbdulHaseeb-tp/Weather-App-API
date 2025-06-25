from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

# Create your views here.

def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'kerala'

    # Weather url setup
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    PARAMS = {'units':'metric'}

    # City image and search engine
    API_KEY = ''
    SEARCH_ENGINE_ID = ''

    query = city + "1920x1080"
    page = 1
    start = (page-1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    # data = requests.get(city_url).json()
    # count = 1
    # search_items = data.get("items")
    # image_url = search_items[1]['link']

    data = requests.get(city_url).json()
    search_items = data.get("items")
    if search_items and len(search_items) > 1:
        image_url = search_items[1]['link']
    elif search_items and len(search_items) > 0:
        image_url = search_items[0]['link']
    else:
        image_url = "https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600"

    try:
        data = requests.get(url,PARAMS).json()

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temperature = data['main']['temp']

        day = datetime.date.today()
        exception_occurred = False

        context = {
            'description': description,
            'icon': icon,
            'temperature': temperature,
            'day': day,
            'city': city,
            'exception_occurred':exception_occurred,
            'image_url':image_url
        }
        return render(request, 'index.html', context)
    except KeyError:
        exception_occurred = True
        day = datetime.date.today()
        messages.error(request, 'Entered data is not available to API')
        context = {
            'day': day,
            'exception_occurred' : exception_occurred,

            'description':'NOTHING',
            'icon': '01d',
            'temperature': 0,
            'city': 'No City Name'
        }
        return render(request, 'index.html', context)