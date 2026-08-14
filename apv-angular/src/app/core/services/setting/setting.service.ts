import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { Setting } from '../../models/Setting';

@Injectable({
  providedIn: 'root'
})
export class SettingService {

  private apiUrl = `${environment.apiUrl}/settings`;

  private settingSubject = new BehaviorSubject<Setting | null>(null);

  setting$ = this.settingSubject.asObservable();

  constructor(private http: HttpClient) { }

   /**
   * Charge le dernier thème depuis le backend
   * et le stocke dans le BehaviorSubject.
   */
  loadSetting(): Observable<Setting> {
    return this.http.get<Setting>(`${this.apiUrl}/latest`).pipe(
      tap(setting => {
        this.settingSubject.next(setting);
      })
    );
  }

   /**
   * Récupérer la valeur actuelle du setting.
   */
  getCurrentSetting(): Setting | null {
    return this.settingSubject.value;
  }

  setSetting(setting: Setting): void {
    this.settingSubject.next(setting);
  }

  addSetting(formData: FormData): Observable<Setting> {
    return this.http.post<Setting>(`${this.apiUrl}`, formData).pipe(
      tap(setting => this.settingSubject.next(setting))
    );
  }

  updateSetting(id: number, formData: FormData): Observable<Setting> {
    return this.http.patch<Setting>(
      `${this.apiUrl}/${id}`,
      formData
    ).pipe(
      tap(setting => this.settingSubject.next(setting))
    );
  }

  deleteSetting(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  getSetting(id: number): Observable<Setting> {
    return this.http.get<Setting>(`${this.apiUrl}/${id}`);
  }

}
