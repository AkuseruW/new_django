from api.routes.AuthRoutes import urlpatterns as auth_urlpatterns
from api.routes.GenderRoutes import urlpatterns as gender_urlpatterns
from api.routes.RelationshipRoutes import urlpatterns as relationship_urlpatterns
from api.routes.UserRoutes import urlpatterns as user_urlpatterns

urlpatterns = []

urlpatterns.extend(auth_urlpatterns)
urlpatterns.extend(gender_urlpatterns)
urlpatterns.extend(relationship_urlpatterns)
urlpatterns.extend(user_urlpatterns)

# urlpatterns = user_urlpatterns + gender_urlpatterns