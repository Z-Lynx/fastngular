// auth.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private baseUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient, private cookieService: CookieService) {}

  login(email: string, password: string) {
    const body = { email, password };
    return this.http.post<any>(`${this.baseUrl}/login`, body);
  }
  
  register(userData: any) {
    return this.http.post<any>(`${this.baseUrl}/register`, userData);
  }

  registerDN(data:any){
    return this.http.post<any>(`${this.baseUrl}/doanh_nghiep/`, data);
  }
  
  registerDNImages(id:any, data:any){
    return this.http.post<any>(`${this.baseUrl}/doanh_nghiep/images?doanh_nghiep_id=${id}`, data);
  }

  info(){
    return this.http.get<any>(`${this.baseUrl}/users/me`,);
  }
  logout(){
    localStorage.clear()
    this.cookieService.deleteAll()
  }
}
