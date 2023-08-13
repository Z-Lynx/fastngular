# app/routes/user.py

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi import File, UploadFile
from typing import List
from pydantic import BaseModel

from apps.demo.models import NguoiDung
from apps.schemas.user import User as UserSchema,  UserCreate, UserUpdate
from apps.database.session import get_db
from apps.schemas import doanhnghiep as schemas
from apps.demo import models
from apps.utils.auth import get_current_user


router = APIRouter()

class Item(BaseModel):
    name: str
    description: str = None

# Định nghĩa API endpoint cho việc POST dữ liệu JSON kèm theo hình ảnh
@router.post("/doanh_nghiep/images")
async def create_item(
    doanh_nghiep_id: int,
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    doanh_nghiep = db.query(models.DoanhNghiep).filter(models.DoanhNghiep.id == doanh_nghiep_id).first()
    
    image_filenames = []
    for image in images:
        filename = f"media/image/{image.filename}"
        with open(filename, "wb") as f:
            contents = await image.read() 
            f.write(contents)
        image_filenames.append(image.filename)
        
    doanh_nghiep.danh_sach_hinh_anh = ";".join(image_filenames)
    db.commit()
    
    return doanh_nghiep
    
@router.post("/doanh_nghiep/")
async def create_doanh_nghiep(
    doanh_nghiep: schemas.DoanhNghiepCreate,
    db: Session = Depends(get_db)
):
    
    last_id = db.query(func.max(models.DoanhNghiep.id)).scalar() or 0
    new_id = last_id + 1
    print("=>" + str(new_id))
    dn = schemas.dctDoanhNghiepCreate(
        ten_doanh_nghiep=doanh_nghiep.ten_doanh_nghiep,
        id_phuong_xa= 9,
        mo_ta=doanh_nghiep.mo_ta,
        dia_chi=doanh_nghiep.dia_chi,
        danh_sach_hinh_anh="",
        trang_thai= 1,
        id_chu_san=doanh_nghiep.id_chu_san,
        id=new_id
    )
    
    # Create the DoanhNghiep object and save it to the database
    db_doanh_nghiep = models.DoanhNghiep(**dn.dict())
    db.add(db_doanh_nghiep)
    db.commit()
    db.refresh(db_doanh_nghiep)
    return db_doanh_nghiep


@router.get("/doanh_nghiep")
def read_doanh_nghiep(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user_data = db.query(NguoiDung).filter(NguoiDung.email == current_user).first()

    
    doanh_nghiep_data = (
        db.query(
            models.DoanhNghiep.dia_chi, 
            models.PhuongXa.ten.label('ten_xa'), 
            models.QuanHuyen.ten.label('ten_quan'), 
            models.TinhThanh.ten.label('ten_tinh'),
            models.DoanhNghiep.id,
            models.DoanhNghiep.ten_doanh_nghiep,   
            models.DoanhNghiep.mo_ta,             
            models.DoanhNghiep.danh_sach_hinh_anh,
        )
        .join(models.PhuongXa, models.DoanhNghiep.id_phuong_xa == models.PhuongXa.id)
        .join(models.QuanHuyen, models.PhuongXa.id_quan_huyen == models.QuanHuyen.id)
        .join(models.TinhThanh, models.QuanHuyen.id_tinh_thanh == models.TinhThanh.id)
        .filter(models.DoanhNghiep.id_chu_san == user_data.id)\
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
        ten_doanh_nghiep,
        mo_ta,
        danh_sach_hinh_anh,
    ) in doanh_nghiep_data:
        dia_chi_formatted = f"{dia_chi}, {ten_xa}, {ten_quan}, {ten_tinh}"
       
        result.append(
            schemas.DoanhNghiep(
                id=id,
                dia_chi=dia_chi_formatted,
                ten_doanh_nghiep=ten_doanh_nghiep,
                mo_ta=mo_ta,
                danh_sach_hinh_anh=danh_sach_hinh_anh,
            )
        )

    return result

@router.get("/doanh_nghiep_small")
def read_doanh_nghiep(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    user_data = db.query(NguoiDung).filter(NguoiDung.email == current_user).first()

    
    doanh_nghiep_data = (
        db.query(
            models.DoanhNghiep.id,
            models.DoanhNghiep.ten_doanh_nghiep,   
        )
        .filter(models.DoanhNghiep.id_chu_san == user_data.id)\
        .all()
    )
    # Process the retrieved data and create a list of DoanhNghiepBase instances
    result = []
    for id, ten_doanh_nghiep in doanh_nghiep_data:
        result.append(
            schemas.DoanhNghiepSmall(
            id_doanh_nghiep=id,
            ten_doanh_nghiep=ten_doanh_nghiep
            )
        )
        
    return result


@router.put("/doanh_nghiep/{doanh_nghiep_id}", response_model=schemas.DoanhNghiep)
def update_doanh_nghiep(
    doanh_nghiep_id: int,
    doanh_nghiep: schemas.DoanhNghiepUpdate,
    db: Session = Depends(get_db)
):
    db_doanh_nghiep = db.query(models.DoanhNghiep).filter(models.DoanhNghiep.id == doanh_nghiep_id).first()
    if not db_doanh_nghiep:
        raise HTTPException(status_code=404, detail="DoanhNghiep not found")
    
    # Update the simple fields from the request
    for key, value in doanh_nghiep.dict().items():
        setattr(db_doanh_nghiep, key, value)
    
    db.commit()
    db.refresh(db_doanh_nghiep)
    return db_doanh_nghiep



@router.delete("/doanh_nghiep/{doanh_nghiep_id}", response_model=schemas.DoanhNghiep)
def delete_doanh_nghiep(doanh_nghiep_id: int, db: Session = Depends(get_db)):
    doanh_nghiep = db.query(models.DoanhNghiep).filter(models.DoanhNghiep.id == doanh_nghiep_id).first()
    if not doanh_nghiep:
        raise HTTPException(status_code=404, detail="DoanhNghiep not found")
    db.delete(doanh_nghiep)
    db.commit()
    return doanh_nghiep



@router.post("/sanbong/")
def create_sanbong(sanbong: schemas.SanBong, db: Session = Depends(get_db)):
    last_id = db.query(func.max(models.SanBong.id)).scalar() or 0
    new_id = last_id + 1
    
    sanbong_data = schemas.SanBongCreate(
        id= new_id,
        id_doanh_nghiep=sanbong.id_doanh_nghiep,
        ten_san_bong=sanbong.ten_san_bong,
        trang_thai=1
    )
    sanbong = models.SanBong(**sanbong_data.dict())
    db.add(sanbong)
    db.commit()
    db.refresh(sanbong)
    return sanbong

@router.get("/sanbongs")
def read_sanbong(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)):
    user_data = db.query(NguoiDung).filter(NguoiDung.email == current_user).first()
    
    sanbong_data = (
        db.query(
            models.SanBong.id, 
            models.SanBong.id_doanh_nghiep, 
            models.SanBong.ten_san_bong, 
            models.SanBong.trang_thai, 
            models.DoanhNghiep.id,
            models.DoanhNghiep.ten_doanh_nghiep,   
            models.DoanhNghiep.id_chu_san,   
        )
        .join(models.SanBong, models.DoanhNghiep.id == models.SanBong.id_doanh_nghiep)
        .filter(models.DoanhNghiep.id_chu_san == user_data.id)\
        .all()
    )
        
    result = []
    
    for id, id_doanh_nghiep, ten_san_bong, trang_thai, id_dn, ten_doanh_nghiep, _ in sanbong_data:
        
        temp = schemas.DoanhNghiepSmall(
            id_doanh_nghiep=id_dn,
            ten_doanh_nghiep=ten_doanh_nghiep
        )
        result.append(
            schemas.SanBongResponse(
                id= id,
                doanh_nghiep= temp,
                ten_san_bong= ten_san_bong,
                trang_thai="Đang hoạt động" if trang_thai != 0 else "Dừng hoạt động"
            )
        )
    return result

@router.get("/sanbong/{sanbong_id}")
def read_sanbong(sanbong_id: int, db: Session = Depends(get_db)):
    sanbong = db.query(models.SanBong).filter(models.SanBong.id == sanbong_id).first()
    if sanbong is None:
        raise HTTPException(status_code=404, detail="SanBong not found")
    return sanbong

@router.put("/sanbong/{sanbong_id}")
def update_sanbong(sanbong_id: int, updated_sanbong: schemas.SanBongUpdate, db: Session = Depends(get_db)):
    sanbong = db.query(models.SanBong).filter(models.SanBong.id == sanbong_id).first()
    if sanbong is None:
        raise HTTPException(status_code=404, detail="SanBong not found")
    
    for key, value in updated_sanbong.dict().items():
        setattr(sanbong, key, value)
        
    db.commit()
    db.refresh(sanbong)
    return sanbong

@router.delete("/sanbong/{sanbong_id}")
def delete_sanbong(sanbong_id: int, db: Session = Depends(get_db)):
    sanbong = db.query(models.SanBong).filter(models.SanBong.id == sanbong_id).first()
    
    if sanbong is None:
        raise HTTPException(status_code=404, detail="SanBong not found")
    
    db.delete(sanbong)
    db.commit()
    return {"message": "SanBong deleted successfully"}