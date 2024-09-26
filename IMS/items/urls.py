from django.urls import path
from .views import CreateItemView, GetItemView, UpdateItemView, DeleteItemView

urlpatterns = [
    path('items/', CreateItemView.as_view(), name='create_item'),
    path('items/<int:item_id>/', GetItemView.as_view(), name='get_item'),
    path('items/<int:item_id>/', UpdateItemView.as_view(), name='update_item'),
    path('items/<int:item_id>/', DeleteItemView.as_view(), name='delete_item'),
]
