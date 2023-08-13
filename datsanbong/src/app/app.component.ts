import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { AuthService } from './service/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  constructor(
    private cookieService: CookieService,
    private authService: AuthService
  ) {}
  ngOnInit(): void {
    if (this.cookieService.get('token_jwt') != '') {
      this.authService.info().subscribe(
        (response) => {
          console.log(response);
          localStorage.setItem('user', JSON.stringify(response));
        },
        (error) => {}
      );
    }
  }
  title = 'datsanbong';
}
