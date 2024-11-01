from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name = 'HomePage'),
    path('snippets/add', views.add_snippet_page, name ='SnippetAdd'),
    path('snippets/list', views.snippets_page, name ='SnippetsList'),
    path('snippets/my', views.my_snippets, name ='MySnippetsList'),
    path('snippets/<int:num>', views.snippet_details, name ='SnippetDetails'),
    path('snippets/<int:num>/edit', views.snippet_edit, name ='SnippetEdit'),
    path('snippets/<int:num>/delete', views.snippet_delete, name ='SnippetDelete'),
    path('login', views.login, name ='login'),
    path('logout', views.logout, name ='logout'),
    path('register', views.create_user, name ='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
