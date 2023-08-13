import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AuthService } from '../service/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
})
export class NavBarComponent implements OnInit {
  isLogin = false;
  userName = '';
  isProfileMenuOpen = false;
  constructor(
    private cookieService: CookieService,
    private authService: AuthService,
    private readonly _router: Router

  ) {}

  toggleProfileMenu() {
    this.isProfileMenuOpen = !this.isProfileMenuOpen;
  }
  ngOnInit() {
    if (this.cookieService.get('token_jwt') != '') {
      this.isLogin = true;
      this.userName = JSON.parse(localStorage.getItem('user')!)['ho_ten'];
    }
  }
  logout() {
    this.authService.logout()
    this._router.navigate(['/home']);
    this.authService.logout()
  }
}
