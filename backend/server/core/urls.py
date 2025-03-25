from django.urls import path, include
from . import views


app_name = 'core'

urlpatterns = [
	path('', views.IndexView.as_view(), name='home'),
	path('category/<slug:category_slug>/', views.IndexView.as_view(), name='category_filter'),
	# path('bucket/', include(bucket_urls)),
	# path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]

