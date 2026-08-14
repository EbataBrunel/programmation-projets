import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, of} from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { EventType } from '../../models/EventType';

@Injectable({
  providedIn: 'root'
})
export class EventTypeService {

  private readonly apiUrl = `${environment.apiUrl}/event-types`;

  constructor(private http: HttpClient) { }

  getEventTypes(): Observable<EventType[]> {
    return this.http.get<EventType[]>(this.apiUrl);
  }

  addEventType(formData: FormData): Observable<EventType> {
    return this.http.post<EventType>(this.apiUrl, formData);
  }

  updateEventType(publicId: string, formData: FormData): Observable<EventType> {
    return this.http.patch<EventType>(`${this.apiUrl}/${publicId}`, formData);
  }

  deleteEventType(publicId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${publicId}`);
  }

  getEventType(publicId: string): Observable<EventType> {
    return this.http.get<EventType>(`${this.apiUrl}/${publicId}`);
  }
}
