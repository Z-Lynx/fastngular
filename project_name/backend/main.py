from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse
from fastapi import FastAPI
from sqlmodel import SQLModel

from fastapi.staticfiles import StaticFiles
from core.adminsite import site
from core.settings import settings

app = FastAPI(debug=settings.debug)
auth = site.auth

# 安装应用
from apps import demo
demo.setup(app.router,site)

# 挂载后台管理系统
site.mount_app(app)

# @app.on_event("startup")
# async def startup():
#     await site.db.async_run_sync(SQLModel.metadata.create_all, is_session=False)
#     # 创建默认管理员,用户名: admin,密码: admin, 请及时修改密码!!!
#     await auth.create_role_user(role_key="admin")

@app.on_event("startup")
async def startup():
    pass

@app.get('/')
async def index():
    return RedirectResponse(url=site.router_path)

app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/image/{filename}")
async def get_image(filename: str):
    # The file path will be /media/{filename}
    return FileResponse(f"media/image/{filename}")

from starlette.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://127.0.0.1:4200",
    "http://localhost:*",
    "http://localhost:3000",
    "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
