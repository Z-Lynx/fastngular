from core.settings import settings
from core.auth import MyAuthAdminSite

from fastapi_amis_admin.admin import AdminSite

# site = AdminSite(settings)

site = MyAuthAdminSite(settings)
auth = site.auth
