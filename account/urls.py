from django.urls import path

# import AccountViewSet
from account.views import AccountViewSet, CustomAuthToken


urlpatterns = [
    path('login', CustomAuthToken.as_view()), # register login/authenticate handler/view
    path('signup',  
    AccountViewSet.as_view({
        'post': 'create'
    })) # register sigin handler
]