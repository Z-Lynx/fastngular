import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AuthService } from '../service/auth.service';

@Component({
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
})
export class TopBarComponent implements OnInit {
  isLogin = false;
  userName = '';
  isProfileMenuOpen = false;
  isChuSan = 0;
  constructor(
    private cookieService: CookieService,
    private authService: AuthService
  ) {}

  toggleProfileMenu() {
    this.isProfileMenuOpen = !this.isProfileMenuOpen;
  }
  ngOnInit() {
    if (this.cookieService.get('token_jwt') != '') {
      this.isLogin = true;
      this.userName = JSON.parse(localStorage.getItem('user')!)['ho_ten'];
      this.isChuSan = JSON.parse(localStorage.getItem('user')!)['id_phan_quyen_nguoi_dung']
    }
  }
  logout() {
    this.authService.logout();
  }
}
