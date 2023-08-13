export interface SanBongField {
  id: number;
  doanh_nghiep: {
    id_doanh_nghiep: number;
    ten_doanh_nghiep: string;
  };
  ten_san_bong: string;
  trang_thai: string;
}

export interface SanBongPostField {
  id_doanh_nghiep: number;
  ten_san_bong: string;
}

export interface SanBongPutField {
  id_doanh_nghiep: number;
  ten_san_bong: string;
  trang_thai: string;
}

export interface SanBongResponseField {
  id: number;
  id_doanh_nghiep:number;
  ten_san_bong: string;
  trang_thai: number;
}
export interface SanBongPustField {
  id_doanh_nghiep: number;
  ten_san_bong: string;
  trang_thai: number;
}
