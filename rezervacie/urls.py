from django.urls import path
from . import views, api

urlpatterns = [
    # auth
    path("login/",    views.login_view,    name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/",   views.logout_view,   name="logout"),

    # index
    path("", views.index, name="index"),

    # admin
    path("admin-panel/",                              views.admin_dashboard,           name="admin_dashboard"),
    path("admin-panel/users/new/",                    views.admin_user_create,         name="admin_user_create"),
    path("admin-panel/users/<int:pk>/edit/",          views.admin_user_edit,           name="admin_user_edit"),
    path("admin-panel/users/<int:pk>/delete/",        views.admin_user_delete,         name="admin_user_delete"),
    path("admin-panel/reservations/<int:pk>/delete/", views.admin_reservation_delete,  name="admin_reservation_delete"),

    # reservations
    path("rezervacie/",                views.reservation_list,   name="reservation_list"),
    path("rezervacie/<int:pk>/",       views.reservation_detail, name="reservation_detail"),
    path("rezervacie/nova/",           views.reservation_create, name="reservation_create"),
    path("rezervacie/<int:pk>/uprav/", views.reservation_edit,   name="reservation_edit"),
    path("rezervacie/<int:pk>/zrus/",  views.reservation_cancel, name="reservation_cancel"),

    # equipment assignment (M:N)
    path("rezervacie/<int:pk>/vybavenie/pridaj/",  views.add_equipment,    name="add_equipment"),
    path("vybavenie-rezervacia/<int:pk>/odstran/", views.remove_equipment, name="remove_equipment"),

    # rooms
    path("miestnosti/",                views.room_list,   name="room_list"),
    path("miestnosti/<int:pk>/",       views.room_detail, name="room_detail"),
    path("miestnosti/nova/",           views.room_create, name="room_create"),
    path("miestnosti/<int:pk>/uprav/", views.room_edit,   name="room_edit"),
    path("miestnosti/<int:pk>/zmaz/",  views.room_delete, name="room_delete"),

    # equipment
    path("vybavenie/",                views.equipment_list,   name="equipment_list"),
    path("vybavenie/nove/",           views.equipment_create, name="equipment_create"),
    path("vybavenie/<int:pk>/uprav/", views.equipment_edit,   name="equipment_edit"),
    path("vybavenie/<int:pk>/zmaz/",  views.equipment_delete, name="equipment_delete"),

    # ── REST API ───────────────────────────────────────────────────────────
    # these return JSON, not HTML
    path("api/miestnosti/",             api.api_room_list,          name="api_room_list"),
    path("api/miestnosti/<int:pk>/",    api.api_room_detail,        name="api_room_detail"),
    path("api/rezervacie/",             api.api_reservation_list,   name="api_reservation_list"),
    path("api/rezervacie/<int:pk>/",    api.api_reservation_detail, name="api_reservation_detail"),
]