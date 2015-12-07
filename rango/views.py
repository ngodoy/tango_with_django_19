from django.shortcuts import render
from django.shortcuts import HttpResponse
from datetime import datetime


from django.views import generic
from rango.models import Category
from rango.models import Page


# Create your views here.



def index(request):

    #request.session.set_test_cookie()

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    print visits
    if not visits:
        visits = 0
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    print last_visit
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    context_dict['visits'] = visits
    request.session['visits'] = visits
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())

    response = render(request,'rango/index.html', context_dict)

    return response

class about(generic.TemplateView):
    template_name = "rango/about.html"


def tempo(request):
    return HttpResponse("Rango says here is the tempo page.")



def category(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            #result_list = run_query(query)
            result_list =[]

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict)
