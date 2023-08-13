// login.component.ts
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { AuthService } from 'src/app/service/auth.service';
import { NgToastService } from 'ng-angular-popup';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
})
export class LoginComponent implements OnInit {
  public loginForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private cookieService: CookieService,
    private authService: AuthService,
    private toast: NgToastService,
    private readonly _router: Router
  ) {}

  ngOnInit(): void {
    this.createLoginForm();
  }

  createLoginForm(): void {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]],
    });
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }

    const email = this.loginForm.value.email;
    const password = this.loginForm.value.password;

    this.authService.login(email, password).subscribe(
      (response) => {
        // Handle the response from the server here (e.g., store token, redirect, etc.)
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
            this._router.navigate(['/home']);
          },
          (error) => {}
        );
      },
      (error) => {
        // Handle error response here
        this.toast.error({
          detail: 'ERROR',
          summary: error.error.detail,
          duration: 5000,
        });
      }
    );
  }
}
