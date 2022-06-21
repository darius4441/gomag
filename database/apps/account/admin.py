# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.forms import Textarea

# from .models import NewUser


# class UserAdminConfig(UserAdmin):
#     model = NewUser
#     search_fields = (
#         "email",
#         "username",
#         "first_name",
#         "last_name",
#         "phone",
#     )
#     list_filter = (
#         "email",
#         "username",
#         "first_name",
#         "last_name",
#         "phone",
#         "is_active",
#         "is_staff",
#     )
#     ordering = ("-start_date",)
#     list_display = (
#         "email",
#         "username",
#         "first_name",
#         "last_name",
#         "phone",
#         "is_active",
#         "is_staff",
#     )
#     fieldsets = (
#         (
#             None,
#             {
#                 "fields": (
#                     "email",
#                     "username",
#                     "first_name",
#                     "last_name",
#                     "phone",
#                 )
#             },
#         ),
#         ("Permissions", {"fields": ("is_staff", "is_active")}),
#         ("Personal", {"fields": ("about",)}),
#     )
#     formfield_overrides = {
#         NewUser.about: {"widget": Textarea(attrs={"rows": 10, "cols": 40})},
#     }
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "email",
#                     "username",
#                     "first_name",
#                     "last_name",
#                     "phone",
#                     "password1",
#                     "password2",
#                     "is_active",
#                     "is_staff",
#                 ),
#             },
#         ),
#     )


# admin.site.register(NewUser, UserAdminConfig)
