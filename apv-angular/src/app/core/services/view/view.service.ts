import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { View } from '../../models/View';

@Injectable({
  providedIn: 'root'
})
export class ViewService {

  private readonly apiUrl = `${environment.apiUrl}/views`;

  constructor(private http: HttpClient) { }

  getViewsByAdmin(): Observable<View[]> {
    return this.http.get<View[]>(`${this.apiUrl}/admin`);
  }

  createMissingViews(): Observable<View> {
    return this.http.post<View>(`${this.apiUrl}/create-missing`, {});
  }

  updateStatusView(): Observable<any> {
    return this.http.patch<any>(
      `${this.apiUrl}/update-status`,
      {}
    );
  }

  getCountUsersNotViewWithAdmin(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/count-view`);
  }

}
