from django.urls import path
from . import views, auth_views

# 'name' lets you do {% url 'index' %} in templates instead of hardcoding "/".
# <int:pk> captures the number from the URL and passes it to the view as pk.

urlpatterns = [
    path("",                                views.index,                name="index"),

    # Rooms
    path("rooms/",                          views.room_list,            name="room_list"),
    path("rooms/<int:pk>/",                 views.room_detail,          name="room_detail"),
    path("rooms/new/",                      views.room_create,          name="room_create"),
    path("rooms/<int:pk>/edit/",            views.room_edit,            name="room_edit"),
    path("rooms/<int:pk>/delete/",          views.room_delete,          name="room_delete"),

    # rezervacie
    path("rezervacie/",                   views.reservation_list,     name="reservation_list"),
    path("rezervacie/<int:pk>/",          views.reservation_detail,   name="reservation_detail"),
    path("rezervacie/new/",               views.reservation_create,   name="reservation_create"),
    path("rezervacie/<int:pk>/edit/",     views.reservation_edit,     name="reservation_edit"),
    path("rezervacie/<int:pk>/cancel/",   views.reservation_cancel,   name="reservation_cancel"),

    # Equipment
    path("equipment/",                      views.equipment_list,       name="equipment_list"),
    path("equipment/new/",                  views.equipment_create,     name="equipment_create"),
    path("equipment/<int:pk>/edit/",        views.equipment_edit,       name="equipment_edit"),
    path("equipment/<int:pk>/delete/",      views.equipment_delete,     name="equipment_delete"),

    #login system
    path("login/",    auth_views.login_view,    name="login"),
    path("register/", auth_views.register_view, name="register"),
    path("logout/",   auth_views.logout_view,   name="logout"),
]
