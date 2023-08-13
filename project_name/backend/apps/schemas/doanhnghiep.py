from pydantic import BaseModel

class DoanhNghiepBase(BaseModel):
    ten_doanh_nghiep: str
    id_phuong_xa: int
    dia_chi: str
    mo_ta: str
    danh_sach_hinh_anh: str
    trang_thai: int

class DoanhNghiepCreate(DoanhNghiepBase):
    id_chu_san: int
    

class dctDoanhNghiepCreate(DoanhNghiepCreate):
    id:int
    
    
class DoanhNghiepUpdate(DoanhNghiepBase):
    pass


class DoanhNghiep(BaseModel):
    id: int
    ten_doanh_nghiep: str
    dia_chi: str
    mo_ta: str
    danh_sach_hinh_anh: str


class DoanhNghiepSmall(BaseModel):
    id_doanh_nghiep: int
    ten_doanh_nghiep: str
    
class SanBong(BaseModel):
    id_doanh_nghiep: int
    ten_san_bong: str

class SanBongResponse(BaseModel):
    id: int
    doanh_nghiep: DoanhNghiepSmall
    ten_san_bong: str
    trang_thai: str
    
class SanBongCreate(SanBong):
    id: int
    trang_thai:int
    
class SanBongUpdate(SanBong):
    trang_thai:int
