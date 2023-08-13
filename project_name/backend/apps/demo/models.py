import sqlmodel
from fastapi_amis_admin import amis
from fastapi_amis_admin.models import Field
from datetime import date, datetime, time

# Create your models here.

class BaseSQLModel(sqlmodel.SQLModel):
    id: int = Field(default=None, primary_key=True, nullable=False)


class Category(BaseSQLModel, table=True):
    __tablename__ = 'blog_category'
    name: str = Field(
        title='Category Name',
        sa_column=sqlmodel.Column(sqlmodel.String(100), unique=True, index=True, nullable=False)
    )
    description: str = Field(default='', title='Description', amis_form_item=amis.Textarea())
    is_active: bool = Field(None, title='Is Active')

class PhanQuyenNguoiDung(BaseSQLModel, table=True):
    __tablename__ = 'phan_quyen_nguoi_dung'
    phan_quyen: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(50), nullable=False)
    )


class TinhThanh(BaseSQLModel, table=True):
    __tablename__ = 'tinh_thanh'
    ten: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(50), nullable=False)
    )


class QuanHuyen(BaseSQLModel, table=True):
    __tablename__ = 'quan_huyen'
    ten: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(50), nullable=False)
    )
    id_tinh_thanh: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('tinh_thanh.id'))
    )


class PhuongXa(BaseSQLModel, table=True):
    __tablename__ = 'phuong_xa'
    ten: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(50), nullable=False)
    )
    id_quan_huyen: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('quan_huyen.id'))
    )


class NguoiDung(BaseSQLModel, table=True):
    __tablename__ = 'nguoi_dung'
    ho_ten: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(20), nullable=False)
    )
    sdt: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(15), nullable=False)
    )
    ngay_sinh: date = Field(sa_column=sqlmodel.Column(sqlmodel.Date))
    email: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(50), nullable=False)
    )
    mat_khau: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(50), nullable=False)
    )
    id_phuong_xa: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('phuong_xa.id'))
    )
    dia_chi: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(50))
    )
    id_phan_quyen_nguoi_dung: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('phan_quyen_nguoi_dung.id'))
    )
    trang_thai: bool = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer)
    )


class DatSan(BaseSQLModel, table=True):
    __tablename__ = 'dat_san'
    id_khach_hang: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('nguoi_dung.id'))
    )
    ngay_thue: date = Field(sa_column=sqlmodel.Column(sqlmodel.Date))
    trang_thai: int = Field(sa_column=sqlmodel.Column(sqlmodel.Integer))


class DoanhNghiep(BaseSQLModel, table=True):
    __tablename__ = 'doanh_nghiep'
    id_chu_san: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('nguoi_dung.id'))
    )
    ten_doanh_nghiep: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(50), nullable=False)
    )
    id_phuong_xa: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('phuong_xa.id'))
    )
    dia_chi: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.Text)
    )
    mo_ta: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.Text)
    )
    danh_sach_hinh_anh: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.Text)
    )
    trang_thai: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer)
    )


class DanhGia(BaseSQLModel, table=True):
    __tablename__ = 'danh_gia'
    id_khach_hang: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('nguoi_dung.id'))
    )
    id_doanh_nghiep: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('doanh_nghiep.id'))
    )
    sao: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer)
    )
    noi_dung: str = Field(
        sa_column=sqlmodel.Column(sqlmodel.String(255))
    )


class SanBong(BaseSQLModel, table=True):
    __tablename__ = 'san_bong'
    id_doanh_nghiep: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('doanh_nghiep.id'))
    )
    ten_san_bong: str = Field(
        title='Ten San Bong',
        sa_column=sqlmodel.Column(sqlmodel.String(50), nullable=False)
    )
    trang_thai: int = Field(
        title='Trang Thai',
        sa_column=sqlmodel.Column(sqlmodel.Integer)
    )


class ThanhToan(BaseSQLModel, table=True):
    __tablename__ = 'thanh_toan'
    id_dat_san: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('dat_san.id'))
    )
    gia_tien: float = Field(
        sa_column=sqlmodel.Column(sqlmodel.DECIMAL(10, 2))
    )
    ngay_thanh_toan: datetime = Field(sa_column=sqlmodel.Column(sqlmodel.DateTime))



class GiaThueSan(BaseSQLModel, table=True):
    __tablename__ = 'gia_thue_san'
    id_san_bong: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('san_bong.id'))
    )
    gio_bat_dau: time = Field(
        sa_column=sqlmodel.Column(sqlmodel.Time, nullable=False)
    )
    gio_ket_thuc: time = Field(
        sa_column=sqlmodel.Column(sqlmodel.Time, nullable=False)
    )
    gia_tien: float = Field(
        sa_column=sqlmodel.Column(sqlmodel.DECIMAL(10, 2), nullable=False)
    )


class ChiTietDatSan(BaseSQLModel, table=True):
    __tablename__ = 'chi_tiet_dat_san'
    id_dat_san: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('dat_san.id'))
    )
    id_gia_thue_san: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer, sqlmodel.ForeignKey('gia_thue_san.id'))
    )
    gia_tien: int = Field(
        sa_column=sqlmodel.Column(sqlmodel.Integer)
    )
