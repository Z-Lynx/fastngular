from datetime import date

from fastapi_amis_admin import admin
from fastapi_amis_admin.amis import PageSchema
from fastapi_amis_admin.models.fields import Field
from fastapi_user_auth.app import UserAuthApp
from fastapi_user_auth.auth.models import CreateTimeMixin, Group, User, UserRoleLink
from fastapi_user_auth.site import AuthAdminSite
from sqlalchemy import String, cast
from sqlalchemy.orm import column_property


class MyUser(User, table=True):
    point: float = Field(default=0)
    phone: str = Field(None, max_length=15)
    parent_id: int = Field(None, foreign_key="auth_user.id")
    birthday: date = Field(None)
    location: str = Field(None)


class MyGroup(Group, table=True):
    __tablename__ = "auth_group"
    icon: str = Field(None)
    is_active: bool = Field(default=True)


class MyGroupAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="Admin", icon="fa fa-group")
    model = MyGroup
    link_model_fields = [Group.roles]
    readonly_fields = ["key"]


class MyUserRoleLink(UserRoleLink, CreateTimeMixin, table=True):
    id: str = Field(
        None,
        sa_column=column_property(
            cast(UserRoleLink.user_id, String)
            + "-"
            + cast(UserRoleLink.role_id, String)
        ),
    )

    description: str = Field(None, title="describe")


class MyUserRoleLinkAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label="user role relationship", icon="fa fa-group")
    model = MyUserRoleLink
    readonly_fields = ["id"]


class MyUserAuthApp(UserAuthApp):
    GroupAdmin = MyGroupAdmin

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_admin(MyUserRoleLinkAdmin)


class MyAuthAdminSite(AuthAdminSite):
    UserAuthApp = MyUserAuthApp
