from api.routes.AuthRoutes import urlpatterns as user_urlpatterns
from api.routes.GenderRoutes import urlpatterns as gender_urlpatterns

urlpatterns = user_urlpatterns + gender_urlpatterns