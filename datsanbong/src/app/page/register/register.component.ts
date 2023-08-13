// login.component.ts
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { AuthService } from 'src/app/service/auth.service';
import { NgToastService } from 'ng-angular-popup';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
})
export class RegisterComponent implements OnInit {
  public registerForm!: FormGroup;
  public registerDNForm!: FormGroup;
  selectedFiles: FileList | undefined;

  constructor(
    private fb: FormBuilder,
    private cookieService: CookieService,
    private authService: AuthService,
    private toast: NgToastService,
    private readonly _router: Router
  ) {}

  onFileChange(event: any) {
    const inputElement = event.target as HTMLInputElement;
    if (inputElement.files) {
      // Wrap the file in an array to create a FileList
      this.selectedFiles = inputElement.files;
    }
  }

  ngOnInit(): void {
    this.createRegisterForm();
    this.createRegisterDNForm();
  }

  createRegisterDNForm(): void {
    this.registerDNForm = this.fb.group({
      ten_doanh_nghiep: ['', [Validators.required]],
      dia_chi: ['', [Validators.required]],
      mo_ta: ['', [Validators.required]],
      hinh_anh: [''],
    });
  }
  createRegisterForm(): void {
    this.registerForm = this.fb.group({
      ho_ten: ['', [Validators.required]],
      sdt: ['', [Validators.required]],
      ngay_sinh: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      dia_chi: ['', [Validators.required]],
      id_phuong_xa: [1],
      mat_khau: ['', [Validators.required]],
      id_phan_quyen_nguoi_dung: [0],
    });
  }
  onSubmit(): void {
    if (this.registerForm.invalid) {
      return;
    }

    if (this.registerForm.value['id_phan_quyen_nguoi_dung'] == true) {
      this.registerForm.value['id_phan_quyen_nguoi_dung'] = 1;
    }

    const formData = this.registerForm.value;
    const formDNData = this.registerDNForm.value;

    var formDataIMG = new FormData();

    for (let i = 0; i < this.selectedFiles!.length; i++) {
      const file: File = this.selectedFiles![i] as File;
      formDataIMG.append('images', file, file.name);
    }

    this.authService.register(formData).subscribe(
      (response) => {
        this.toast.success({
          detail: 'SUCCESS',
          summary: 'Đăng nhập thành công',
          duration: 5000,
        });
        this.cookieService.set('token_jwt', response.access_token);
        this.authService.info().subscribe(
          (response) => {
            console.log(response);
            localStorage.setItem('user', JSON.stringify(response));
            var data = {
              ten_doanh_nghiep: formDNData['ten_doanh_nghiep'],
              id_phuong_xa: 9,
              dia_chi: formDNData['dia_chi'],
              mo_ta: formDNData['mo_ta'],
              danh_sach_hinh_anh: '',
              trang_thai: 1,
              id_chu_san: response['id'],
            };

            this.authService.registerDN(data).subscribe(
              (response) => {
                this.authService
                  .registerDNImages(response['id'], formDataIMG)
                  .subscribe();
                this._router.navigate(['/home']);
              },
              (error) => {}
            );
          },
          (error) => {}
        );
      },
      (error) => {
        // Handle error response here, e.g., show an error message
        this.toast.error({
          detail: 'ERROR',
          summary: error.error.detail,
          duration: 5000,
        });
      }
    );
  }
}
