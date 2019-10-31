# Create your views here.
from django.shortcuts import render
from wagtail.core.models import Page
from wagtail.search.models import Query

from blog.models import BlogArticlePage
from blog.models import BlogIndexPage


def search(request):
    search_query = request.GET.get("phrase", None)
    if search_query:
        articles_results = BlogArticlePage.objects.live().search(search_query)
        articles_page_ids = [p.page_ptr.id for p in articles_results]
        search_results = Page.objects.live().filter(id__in=articles_page_ids)

        query = Query.get(search_query)

        # Record hit
        query.add_hit()
    else:
        search_results = Page.objects.none()

    return render(
        request,
        "search/search_results.haml",
        {"search_query": search_query, "search_results": search_results, "page": BlogIndexPage.objects.all().last()},
    )
