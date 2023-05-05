from django.urls import path, include

from djangoFinal.blog import views
from djangoFinal.blog.views import blog_index, display_blog_post, create_comment, signup, contact_view, thank_you, \
    login_page, logout_page, newsletter_view

urlpatterns = [
    # path(r'^post/', views.display_blog, name='post_index')
    # path('/', views.display_blog_post, name='post_detail')
    # path('tag/<slug:tag_slug>/', display_blog_post, name='post_list_by_tag'),
    path('', blog_index, name='blog_page'),
    path('<slug:post>/', display_blog_post, name='post_detail'),
    path('create-comment/<slug:post>/', create_comment, name='create_comment'),

]