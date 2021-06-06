from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from market import views
from market.views import ProductListView, ProductListViewByCategory

app_name = 'market'

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='product_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        ProductListViewByCategory.as_view(),
        name='product_list_by_category'),
    url(r'^(?P<id_>\d+)/(?P<slug>[-\w]+)/$',
        views.product_detail,
        name='product_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
