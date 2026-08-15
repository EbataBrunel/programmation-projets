import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, of } from 'rxjs';
import { News } from '../../models/News';
import { environment } from 'src/app/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class NewsService {

  private apiUrl = `${environment.apiUrl}/news`;

  constructor(private http: HttpClient) { }

  getAllNews(): Observable<News[]> {
    return this.http.get<News[]>(`${this.apiUrl}`).pipe(
      catchError(error => {
        console.error('Erreur API news', error);
        return of([]); // empêche Angular de planter
      })
    );
  }

  addNews(formData: FormData): Observable<News> {
    return this.http.post<News>(`${this.apiUrl}`, formData);
  }

  updateNews(publicId: string, formData: FormData): Observable<News> {
    return this.http.patch<News>(`${this.apiUrl}/${publicId}`, formData);
  }

  deleteNews(publicId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${publicId}`);
  }

  getNews(publicId: string): Observable<News> {
    return this.http.get<News>(`${this.apiUrl}/${publicId}`);
  }
}
