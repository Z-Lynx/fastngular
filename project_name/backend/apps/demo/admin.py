from fastapi_amis_admin import amis, admin
from fastapi_amis_admin.admin import AdminApp

from .models import *

class AddressApp(admin.AdminApp):
    page_schema = amis.PageSchema(label='Address', icon='fa fa-location-dot')
    router_prefix = '/address'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.register_admin(TinhThanhAdmin)
        self.register_admin(QuanHuyenAdmin)
        self.register_admin(PhuongXaAdmin)

class FootBallApp(admin.AdminApp):
    page_schema = amis.PageSchema(label='FootBall', icon='fa fa-futbol')
    router_prefix = '/football'

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        # self.register_admin(CategoryAdmin)
        self.register_admin(NguoiDungAdmin)
        self.register_admin(PhanQuyenNguoiDungAdmin)
        self.register_admin(DatSanAdmin)
        self.register_admin(DoanhNghiepAdmin)
        self.register_admin(DanhGiaAdmin)
        self.register_admin(SanBongAdmin)
        self.register_admin(ThanhToanAdmin)
        self.register_admin(GiaThueSanAdmin)
        self.register_admin(ChiTietDatSanAdmin)


# Register your models here.

# class CategoryAdmin(admin.ModelAdmin):
#     page_schema = amis.PageSchema(label='Category', icon='fa fa-folder')
#     model = Category
#     search_fields = [Category.name]


class NguoiDungAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='NguoiDung', icon='fa fa-user')
    model = NguoiDung
    search_fields = [NguoiDung.ho_ten]
    
class PhanQuyenNguoiDungAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='PhanQuyen', icon='fa fa-shield-halved')
    model = PhanQuyenNguoiDung
    search_fields = [PhanQuyenNguoiDung.phan_quyen]


class TinhThanhAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='TinhThanh', icon='fa fa-folder')
    model = TinhThanh
    search_fields = [TinhThanh.ten]


class QuanHuyenAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='QuanHuyen', icon='fa fa-folder')
    model = QuanHuyen
    search_fields = [QuanHuyen.ten]


class PhuongXaAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='PhuongXa', icon='fa fa-folder')
    model = PhuongXa
    search_fields = [PhuongXa.ten]


class DatSanAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='DatSan', icon='fa fa-book')
    model = DatSan
    search_fields = [DatSan.id_khach_hang]


class DoanhNghiepAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='DoanhNghiep', icon='fa fa-briefcase')
    model = DoanhNghiep
    search_fields = [DoanhNghiep.ten_doanh_nghiep]


class DanhGiaAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='DanhGia', icon='fa fa-comment')
    model = DanhGia
    search_fields = [DanhGia.id_khach_hang, DanhGia.id_doanh_nghiep]


class SanBongAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='SanBong', icon='fa fa-clone')
    model = SanBong
    search_fields = [SanBong.ten_san_bong]


class ThanhToanAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='ThanhToan', icon='fa fa-wallet')
    model = ThanhToan
    search_fields = [ThanhToan.id_dat_san]


class GiaThueSanAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='GiaThueSan', icon='fa fa-hand-holding-dollar')
    model = GiaThueSan
    search_fields = [GiaThueSan.id_san_bong]


class ChiTietDatSanAdmin(admin.ModelAdmin):
    page_schema = amis.PageSchema(label='ChiTietDatSan', icon='fa fa-circle-info')
    model = ChiTietDatSan
    search_fields = [ChiTietDatSan.id_dat_san, ChiTietDatSan.id_gia_thue_san]
    
    
