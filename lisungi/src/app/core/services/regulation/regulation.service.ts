import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, of } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { Regulation } from '../../models/Regulation';

@Injectable({
  providedIn: 'root'
})
export class RegulationService {

  private readonly apiUrl = `${environment.apiUrl}/regulations`;

    constructor(private http: HttpClient) { }

    getRegulations(): Observable<Regulation[]> {
      return this.http.get<Regulation[]>(this.apiUrl);
    }

    addRegulation(formData: FormData): Observable<Regulation> {
      return this.http.post<Regulation>(`${this.apiUrl}`, formData);
    }

    updateRegulation(publicId: string, formData: FormData): Observable<Regulation> {
      return this.http.patch<Regulation>(
        `${this.apiUrl}/${publicId}`,
        formData
      );
    }

    deleteRegulation(publicId: string): Observable<any> {
      return this.http.delete(`${this.apiUrl}/${publicId}`);
    }

    getRegulation(publicId: string): Observable<Regulation> {
      return this.http.get<Regulation>(`${this.apiUrl}/${publicId}`);
    }
}
