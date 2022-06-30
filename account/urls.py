from django.urls import path


# import AccountViewSet
from account.views import AccountViewSet, AccountViewSetUpdate, CustomAuthToken


urlpatterns = [
    path('login', CustomAuthToken.as_view()), # register login/authenticate handler/view
    path('signup',  
    AccountViewSet.as_view({
        'post': 'create'
    }),), # register sigin handler
    path('account', AccountViewSetUpdate.as_view({ 'put': 'update', 'get': 'retrieve'}))
]