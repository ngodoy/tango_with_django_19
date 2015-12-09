from django.shortcuts import render
from django.shortcuts import HttpResponse
from datetime import datetime
from django.views import generic

from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm

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


class category(generic.DetailView):
    model = Category
    slug_url_kwarg = "category_name_slug"
    template_name = "rango/category.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
            context = super(category, self).get_context_data(**kwargs)
            pages = Page.objects.filter(category=context['category']).order_by('-views')
            context['pages'] = pages
            if 'query' in context:
                context['query'] = context['category'].name
            return context

    def post(self, request, *args, **kwargs):
        context = super(category, self).get_context_data(**kwargs)
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            #result_list = run_query(query)
            result_list =[]
            context['result_list'] = result_list
            context['query'] = query

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

class add_page(generic.UpdateView):
    #return render(request, 'rango/add_page.html', {'form':form, 'category': cat})
    form_class = PageForm
    template_name = "rango/add_page.html"
    model = Category
    slug_url_kwarg = "category_name_slug"
    context_object_name = "category"

    def get_success_url(self):
        return reverse('category', kwargs={'category_name_slug': self.object.slug,})

    def form_valid(self, form):
        cat = self.get_object()
        page = form.save(commit=False)
        page.category = cat
        page.views = 0
        page.save()
        print page.id
        return HttpResponseRedirect(self.get_success_url())
