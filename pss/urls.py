from django.urls import path
from .views import *

urlpatterns = [
    #path('', CommonView.as_view(), name='index'),
    path('login/', loginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('newuser/', new_user, name='new_user'),
    path('', ProjectView.as_view(), name='index'),
    path('del/',delete, name='delete'),
    path('vav/',VAV.as_view(), name='vav'),
    path('r/',read, name='read'),
    path('test/',test, name='test'),
    path('save/',save_project, name='save'),
    path('disp/',disp, name='disp'),
    path('ld/',lost_damage, name='lost_damage'),
    path('i/',inventory, name='inventory'),
    path('p/', ProjectView.as_view(), name='project'),
    path('a/',activities, name='activities'),
    path('download/',download_file),
    path('grd/',GRD.as_view(), name='grd'),
    #path('u/',construction, name='update'),
    ]

"""

#Uncomment this block while system maintenance
urlpatterns = [
    path('', maintenance, name='index'),
    path('p/',maintenance, name='perso'),    
    path('r/',maintenance, name='read'),
    path('ld/',maintenance, name='lost_damage'),
    path('i/',maintenance, name='inventory'),
    path('s/', maintenance, name='setting'),
    path('s/create_mifare_profile',maintenance,name='create_mifare_profile'),
    path('a/',maintenance, name='activities'),
    path('u/',maintenance, name='update'),
    path('login/',maintenance,name='login')
    ]

"""