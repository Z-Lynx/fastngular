// football-field.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FootballField } from './football-field.model';

@Injectable({
  providedIn: 'root'
})
export class FootballFieldService {
  private apiUrl = 'http://127.0.0.1:8000/doanh-nghiep?skip=0&limit=100'; // Replace 'YOUR_API_URL' with the actual API endpoint.

  constructor(private http: HttpClient) {}

  getFootballFields(): Observable<FootballField[]> {
    return this.http.get<FootballField[]>(this.apiUrl);
  }
}
