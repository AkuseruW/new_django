from django.urls import path

from api.views.RelationshipView import RelationshipViewSet

urlpatterns = [
    path(
        "relationship/",
        RelationshipViewSet.as_view({"get": "list", "post": "create"}),
        name="relationship_list",
    ),
    path(
        "relationship/<int:pk>/",
        RelationshipViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="relationship_detail",
    ),
]
