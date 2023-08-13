// football-field.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DoanhNghiepField } from './doanhnghiep-field.model';

@Injectable({
  providedIn: 'root'
})
export class DoanhNghiepFieldService {
  private apiUrl = 'http://127.0.0.1:8000/doanh_nghiep'; // Replace 'YOUR_API_URL' with the actual API endpoint.

  constructor(private http: HttpClient) {}

  getDoanhNghiepFields(): Observable<DoanhNghiepField[]> {
    return this.http.get<DoanhNghiepField[]>(this.apiUrl);
  }
}
