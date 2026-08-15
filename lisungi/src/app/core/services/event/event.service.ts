import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Event } from '../../models/Event';
import { EventTypeCount } from '../../models/EventTypeCount';
import { environment } from 'src/app/environments/environment';
import { EventCountByYear } from '../../models/EventCountByYear';

@Injectable({
  providedIn: 'root'
})
export class EventService {

  private readonly apiUrl = `${environment.apiUrl}/events`;

    constructor(private http: HttpClient) { }

    getEvents(): Observable<Event[]> {
      return this.http.get<Event[]>(this.apiUrl);
    }

    addEvent(event: Event): Observable<Event> {
      return this.http.post<Event>(this.apiUrl, event);
    }

    getCountEventsByEventType(): Observable<EventTypeCount[]>{
      return this.http.get<EventTypeCount[]>(`${this.apiUrl}/count/event`);
    }

    findEventsByEventTypeId(eventTypeId: any): Observable<Event[]>{
      return this.http.get<Event[]>(`${this.apiUrl}/events/${eventTypeId}`);
    }

    updateClosureStatusEvent(publicId: string, data: any): Observable<Event> {
      return this.http.patch<Event>(
        `${this.apiUrl}/update-closure-status/${publicId}`,
        data
      );
    }

    updateEvent(event: Event): Observable<Event> {
      return this.http.patch<Event>(
        `${this.apiUrl}/${event.publicId}`,
        event
      );
    }

    deleteEvent(publicId: string): Observable<any> {
      return this.http.delete(`${this.apiUrl}/${publicId}`);
    }

    getEvent(publicId: string): Observable<Event> {
      return this.http.get<Event>(`${this.apiUrl}/${publicId}`);
    }

    getEventById(id: number): Observable<Event> {
      return this.http.get<Event>(`${this.apiUrl}/id/${id}`);
    }

    getEventsByYear(year: number): Observable<Event[]> {

      const params = new HttpParams()
        .set('year', year);

      return this.http.get<Event[]>(
        `${this.apiUrl}/year`,
        { params }
      );
    }

    getEventsByMonth(year: number, month: number): Observable<Event[]> {

      const params = new HttpParams()
        .set('year', year)
        .set('month', month);

      return this.http.get<Event[]>(
        `${this.apiUrl}/month`,
        { params }
      );
    }

    countEventsByYear(): Observable<EventCountByYear[]> {
      return this.http.get<EventCountByYear[]>(
        `${this.apiUrl}/statistics/by-year`
      );
    }
}
