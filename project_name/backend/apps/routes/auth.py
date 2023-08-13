# app/routes/NguoiDung.py

import bcrypt
from sqlalchemy import func
from jose import JWTError, jwt
from typing import Annotated, List
from sqlalchemy.orm import joinedload, Session
from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException

from apps.demo.models import *
from apps.database.session import get_db
from apps.schemas.auth import Token, authenticate_user
from apps.utils.auth import create_access_token, get_current_user
from apps.schemas.user import  DoanhNghiepBase, UserCreate, UserLogin, UserUpdate, UserSmall, UserBase

router = APIRouter()

async def get_current_active_user(
    current_user: Annotated[NguoiDung, Depends(get_current_user)],
    db: Session = Depends(get_db)
    ):
    
    current_user = db.query(NguoiDung).filter(NguoiDung.email == current_user).first()
    if current_user.trang_thai != 1:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

ACCESS_TOKEN_EXPIRE_DAYS = 30

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Get NguoiDung registration data from the user_data parameter
    email = user_data.email
    password = user_data.mat_khau

    # Check if the username or email already exists in the database
    nguoi_dung_by_email = db.query(NguoiDung).filter(NguoiDung.email == email).first()
    if nguoi_dung_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new NguoiDung in the database
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    last_id = db.query(func.max(NguoiDung.id)).scalar() or 0
    new_id = last_id + 1
    new_user = NguoiDung(
        id= new_id,
        email=email,
        mat_khau=hashed_password,
        ho_ten=user_data.ho_ten,
        sdt=user_data.sdt,
        ngay_sinh=user_data.ngay_sinh,
        id_phuong_xa=user_data.id_phuong_xa,
        dia_chi=user_data.dia_chi,
        id_phan_quyen_nguoi_dung=user_data.id_phan_quyen_nguoi_dung,
        trang_thai=1
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create a JWT for the NguoiDung with an expiration time of 30 days
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"email": email}, expires_delta=access_token_expires
    )

    # Return the JWT
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: UserLogin, db: Session = Depends(get_db)):
    # Get NguoiDung login data from the form
    username = form_data.email
    password = form_data.password

    # Check if the username exists in the database
    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.email == username).first()
    if not nguoi_dung:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Check if the password is correct
    if not bcrypt.checkpw(password.encode("utf-8"), nguoi_dung.mat_khau.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Create a JWT for the NguoiDung with an expiration time of 30 days
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"email": username}, expires_delta=access_token_expires
    )
    
    # Return the JWT
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/change-info", response_model=UserUpdate)
async def change_info(user_data: UserUpdate, db: Session = Depends(get_db), current_user: NguoiDung = Depends(get_current_user)):
    # Decode and verify the JWT token
    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.email == current_user).first()
    if not nguoi_dung:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's information
    nguoi_dung.ho_ten = user_data.ho_ten
    nguoi_dung.sdt = user_data.sdt
    nguoi_dung.ngay_sinh = user_data.ngay_sinh
    nguoi_dung.id_phuong_xa = user_data.id_phuong_xa
    nguoi_dung.dia_chi = user_data.dia_chi

    # Commit the changes to the database
    db.commit()

    # Return the updated user information
    return user_data


@router.get("/users/me")
def read_users_me(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user_data = db.query(NguoiDung).filter(NguoiDung.email == current_user).first()
    return {
            "id":user_data.id,
            "ho_ten": user_data.ho_ten,
            "sdt": user_data.sdt,
            'ngay_sinh': user_data.ngay_sinh,
            "email":user_data.email,
            'dia_chi': user_data.dia_chi,
            'id_phuong_xa': user_data.id_phuong_xa,
            'id_phan_quyen_nguoi_dung': user_data.id_phan_quyen_nguoi_dung
        }

@router.get("/doanh-nghiep", response_model=List[DoanhNghiepBase])
def read_all_doanh_nghiep(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Query the DoanhNghiep table and join the related tables to get the required information.
    doanh_nghiep_data = (
        db.query(
            DoanhNghiep.dia_chi, 
            PhuongXa.ten.label('ten_xa'), 
            QuanHuyen.ten.label('ten_quan'), 
            TinhThanh.ten.label('ten_tinh'),
            DoanhNghiep.id,
            NguoiDung.id.label('id_user'),
            DoanhNghiep.ten_doanh_nghiep,    # Include this field in the query
            DoanhNghiep.mo_ta,               # Include this field in the query
            DoanhNghiep.danh_sach_hinh_anh,  # Include this field in the query
        )
        .join(NguoiDung, DoanhNghiep.id_chu_san == NguoiDung.id)
        .join(PhuongXa, DoanhNghiep.id_phuong_xa == PhuongXa.id)
        .join(QuanHuyen, PhuongXa.id_quan_huyen == QuanHuyen.id)
        .join(TinhThanh, QuanHuyen.id_tinh_thanh == TinhThanh.id)
        .filter(DoanhNghiep.trang_thai != 0)
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Process the retrieved data and create a list of DoanhNghiepBase instances
    result = []
    for (
        dia_chi,
        ten_xa,
        ten_quan,
        ten_tinh,
        id,
        id_user,
        ten_doanh_nghiep,
        mo_ta,
        danh_sach_hinh_anh,
    ) in doanh_nghiep_data:
        dia_chi_formatted = f"{dia_chi}, {ten_xa}, {ten_quan}, {ten_tinh}"
        user_data = db.query(NguoiDung).filter(NguoiDung.id == id_user).first()
        # Create a UserSmall instance and populate its fields
        user_small = UserSmall(
            ho_ten=user_data.ho_ten,
            sdt=user_data.sdt,
        )
        result.append(
            DoanhNghiepBase(
                id=id,
                user= user_small,
                dia_chi=dia_chi_formatted,
                ten_doanh_nghiep=ten_doanh_nghiep,
                mo_ta=mo_ta,
                danh_sach_hinh_anh=danh_sach_hinh_anh,
            )
        )

    return result

@router.post("/token", response_model=Token)  # Use the Token model as the response model
async def login_for_access_token(form_data: UserLogin, db: Session = Depends(get_db)):
    # Get NguoiDung login data from the form
    username = form_data.email
    password = form_data.password
    
    # Check if the username exists in the database
    nguoi_dung = db.query(NguoiDung).filter(NguoiDung.email == username).first()
    if not nguoi_dung:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Check if the password is correct
    if not bcrypt.checkpw(password.encode("utf-8"), nguoi_dung.mat_khau):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"email": username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
