# app/schemas/user.py

from typing import Optional
from datetime import date
from pydantic import BaseModel

class UserBase(BaseModel):
    ho_ten: str
    sdt: str
    ngay_sinh: date
    email: str
    dia_chi: str
    id_phuong_xa: int
    id_phan_quyen_nguoi_dung: int

class UserCreate(UserBase):
    ho_ten: str
    sdt: str
    ngay_sinh: date
    email: str
    dia_chi: str
    id_phuong_xa: int
    mat_khau: str
    id_phan_quyen_nguoi_dung: int

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserUpdate(UserBase):
    ho_ten: str
    sdt: str
    ngay_sinh: date
    dia_chi: str
    id_phuong_xa: int

class User(UserBase):
    id: int
    id_phuong_xa: int

class UserSmall(BaseModel):
    ho_ten: str
    sdt: str

class DoanhNghiepBase(BaseModel):
    id: int
    user: UserSmall
    ten_doanh_nghiep: str
    dia_chi: str
    mo_ta: str
    danh_sach_hinh_anh: str
  
class DoanhNghiep(DoanhNghiepBase):
    id: int
    id_chu_san: int
    id_phuong_xa: int
    trang_thai: int

    class Config:
        orm_mode = True