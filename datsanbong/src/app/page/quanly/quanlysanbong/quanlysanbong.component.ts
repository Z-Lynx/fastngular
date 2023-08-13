import { Component, OnInit } from '@angular/core';
import { SanBongField } from './quanlysanbong-field.model';
import { SanBongFieldService } from './quanlysanbong-field.service';
import { NgToastService } from 'ng-angular-popup';
import { Router } from '@angular/router';
import { DoanhNghiepSmallField } from './popup-field.model';

@Component({
  selector: 'app-quanlysanbong',
  templateUrl: './quanlysanbong.component.html',
  styleUrls: ['./quanlysanbong.component.scss'],
})
export class QuanlysanbongComponent implements OnInit {
  trangThais = [
    { value: '0', label: 'Dừng Hoạt động' },
    { value: '1', label: 'Đang Hoạt động' },
  ];

  doanhNghiepSmallField: DoanhNghiepSmallField[] = [];
  sanBongFields: SanBongField[] = [];
  selectedDoanhNghiep: any;
  selectedTrangThai: any;
  tenSanBong: any;
  showPopup = false;
  showEditPopup = false;
  saveEdit = false;
  tempsanBongField: any;
  showDelPopup = false;

  openPopup() {
    this.showPopup = true;
  }

  closePopup() {
    this.showPopup = false;
    this.showEditPopup = false;
    this.showDelPopup = false;
  }

  getDoanhNghiepSmallFields(): void {
    this.sanBongFieldService
      .getDoanhNghiepSmallFields()
      .subscribe((items: DoanhNghiepSmallField[]) => {
        for (let item of items) {
          const doanhNghiep: DoanhNghiepSmallField = {  
            id_doanh_nghiep: item.id_doanh_nghiep,
            ten_doanh_nghiep: item.ten_doanh_nghiep,
          };

          // Kiểm tra xem doanh nghiệp đã tồn tại trong mảng chưa
          const existingDoanhNghiep = this.doanhNghiepSmallField.find(
            (dn) => dn.id_doanh_nghiep === doanhNghiep.id_doanh_nghiep
          );
          if (!existingDoanhNghiep) {
            this.doanhNghiepSmallField.push(doanhNghiep);
          }
        }
      });
  }
  addData() {
    console.log('Doanh Nghiệp:', this.selectedDoanhNghiep);
    console.log('Tên Sân Bóng:', this.tenSanBong);

    this.sanBongFieldService
      .postSanBongField({
        id_doanh_nghiep: this.selectedDoanhNghiep,
        ten_san_bong: this.tenSanBong,
      })
      .subscribe(
        (response) => {
          this.toast.success({
            detail: 'SUCCESS',
            summary: 'Thêm thành công',
            duration: 5000,
          });
          this.showPopup = false;
          console.log(response);
          var ten_san_bong = '';
          var trang_thai = 'Dừng hoạt động';

          if (response.trang_thai == 1) {
            trang_thai = 'Đang hoạt động';
          }

          for (let item of this.doanhNghiepSmallField) {
            if (item.id_doanh_nghiep == response.id_doanh_nghiep) {
              ten_san_bong = item.ten_doanh_nghiep;
              break;
            }
          }

          this.sanBongFields.push({
            id: response.id,
            doanh_nghiep: {
              id_doanh_nghiep: response.id_doanh_nghiep,
              ten_doanh_nghiep: ten_san_bong,
            },
            ten_san_bong: response.ten_san_bong,
            trang_thai: trang_thai,
          });
          this.showPopup = false;
          this.showEditPopup = false;
        },
        (error) => {
          this.toast.error({
            detail: 'ERROR',
            summary: 'Lỗi Serve',
            duration: 5000,
          });
        }
      );
  }

  constructor(
    private sanBongFieldService: SanBongFieldService,
    private toast: NgToastService,
    private readonly _router: Router
  ) {}

  ngOnInit(): void {
    this.getFootballFields();
    this.getDoanhNghiepSmallFields();
  }

  getFootballFields(): void {
    this.sanBongFieldService
      .getSanBongFields()
      .subscribe((fields: SanBongField[]) => {
        this.sanBongFields = fields;
      });
  }

  onEdit(sanBongField: SanBongField) {
    this.showEditPopup = true;
    this.selectedDoanhNghiep = sanBongField.doanh_nghiep.id_doanh_nghiep;
    this.tenSanBong = sanBongField.ten_san_bong;
    var id_trang_thai = 0;
    if (sanBongField.trang_thai == 'Đang hoạt động') {
      id_trang_thai = 1;
    }
    this.selectedTrangThai = id_trang_thai;
    this.tempsanBongField = sanBongField;
  }

  saveData() {
    this.sanBongFieldService
      .putSanBongField(this.tempsanBongField.id, {
        id_doanh_nghiep: this.selectedDoanhNghiep,
        ten_san_bong: this.tenSanBong,
        trang_thai: this.selectedTrangThai,
      })
      .subscribe(
        (response) => {
          this.toast.success({
            detail: 'SUCCESS',
            summary: 'Cập nhập thành công',
            duration: 5000,
          });
          this.showPopup = false;

          const index = this.sanBongFields.findIndex(
            (item) => item.id === this.tempsanBongField.id
          );
          var ten_san_bong = '';

          for (let item of this.doanhNghiepSmallField) {
            if (item.id_doanh_nghiep == response.id_doanh_nghiep) {
              ten_san_bong = item.ten_doanh_nghiep;
              break;
            }
          }
          if (index !== -1) {
            // Tìm thấy phần tử trong mảng
            const responseSanBongField = this.sanBongFields[index];
            responseSanBongField.doanh_nghiep.id_doanh_nghiep =
              this.selectedDoanhNghiep;
            responseSanBongField.ten_san_bong = this.tenSanBong;

            // Cập nhật trạng thái dựa vào response từ API
            if (response.trang_thai == 1) {
              responseSanBongField.trang_thai = 'Đang hoạt động';
            } else {
              responseSanBongField.trang_thai = 'Dừng hoạt động';
            }

            // Tìm và gán tên doanh nghiệp dựa vào id_doanh_nghiep từ response
            for (const item of this.doanhNghiepSmallField) {
              if (item.id_doanh_nghiep === response.id_doanh_nghiep) {
                responseSanBongField.doanh_nghiep.ten_doanh_nghiep =
                  item.ten_doanh_nghiep;
                break;
              }
            }
          }
          this.showPopup = false;
          this.showEditPopup = false;
        },
        (error) => {
          this.toast.error({
            detail: 'ERROR',
            summary: 'Lỗi Serve',
            duration: 5000,
          });
        }
      );
  }
  onDelete(sanBongField: SanBongField) {
    console.log('Delete:', sanBongField);
    this.tenSanBong = sanBongField.ten_san_bong;
    this.showDelPopup = true;
    this.tempsanBongField = sanBongField;
  }

  delData() {
    this.sanBongFieldService
      .deleteSanBongField(this.tempsanBongField.id)
      .subscribe(
        (response) => {
          this.toast.success({
            detail: 'SUCCESS',
            summary: 'Xóa thành công',
            duration: 5000,
          });
          const index = this.sanBongFields.findIndex(
            (item) => item.id === this.tempsanBongField.id
          );
          if (index !== -1) {
            this.sanBongFields.splice(index, 1);
          }
          this.showDelPopup = false;
        },
        (error) => {
          this.toast.error({
            detail: 'ERROR',
            summary: 'Lỗi Serve',
            duration: 5000,
          });
        }
      );
  }
}
