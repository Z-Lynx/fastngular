from fastapi import APIRouter
from fastapi_amis_admin.admin import AdminApp
from ..routes import auth as authRouter
from ..routes import user as userRouter

def setup(router: APIRouter, admin_app: AdminApp, **kwargs):
    # 导入相关模块
    from . import admin, apis

    # 注册路由
    router.include_router(apis.router, prefix='/demo', tags=['Demo'])
    router.include_router(authRouter.router, prefix='')
    router.include_router(userRouter.router, prefix='')
    
    # 注册管理页面
    admin_app.register_admin(admin.AddressApp)
    admin_app.register_admin(admin.FootBallApp)

