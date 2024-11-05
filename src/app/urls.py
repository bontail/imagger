from django.urls import path
from app.views import CreateImageView, GetAllImagesView, GetUserImagesView, \
    UpdateImageView, GetAllTagsView, GetImageView, DeleteImageView

urlpatterns = [
    path('create_image/', CreateImageView.as_view()),
    path('get_image/<id>', GetImageView.as_view()),
    path('update_image/<id>', UpdateImageView.as_view()),
    path('delete_image/<id>', DeleteImageView.as_view()),

    path('get_all_images/', GetAllImagesView.as_view()),
    path('get_user_images/<user_id>', GetUserImagesView.as_view()),

    path('get_tags/', GetAllTagsView.as_view()),
]
