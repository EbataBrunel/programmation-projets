import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { Contribution } from '../../models/Contribution';
import { ContributionsByEventCount } from '../../models/ContributionsByEventCount';
import { EventTypeContributionCount } from '../../models/EventTypeContributionCount';
import { ContributedCount } from '../../models/ContributedCount';
import { ContributionCountByEventType } from '../../models/ContributionCountByEventType';

@Injectable({
  providedIn: 'root'
})
export class ContributionService {
    private readonly apiUrl = `${environment.apiUrl}/contributions`;

    constructor(private http: HttpClient) { }

    getContributions(): Observable<Contribution[]> {
      return this.http.get<Contribution[]>(this.apiUrl);
    }

    addContribution(formData: FormData): Observable<Contribution> {
      return this.http.post<Contribution>(this.apiUrl, formData);
    }

    updateContribution(publicId: string, formData: FormData): Observable<Contribution> {
      return this.http.patch<Contribution>(
        `${this.apiUrl}/${publicId}`,
        formData
      );
    }

    deleteContribution(publicId: string): Observable<any> {
      return this.http.delete(`${this.apiUrl}/${publicId}`);
    }

    getContribution(publicId: string): Observable<Contribution> {
      return this.http.get<Contribution>(`${this.apiUrl}/${publicId}`);
    }

    getContributionByEvent(publicId: string): Observable<Contribution[]> {
        return this.http.get<Contribution[]>(`${this.apiUrl}/event/${publicId}`);
    }

    getContributionsByContributed(publicId: string): Observable<Contribution[]> {
        return this.http.get<Contribution[]>(`${this.apiUrl}/contributed/${publicId}`);
    }

    getCountContributionsByContributed(): Observable<ContributedCount[]>{
      return this.http.get<ContributedCount[]>(`${this.apiUrl}/grouped-by-contributed`);
    }

    getCountEventByEventTypeWithContribution(): Observable<EventTypeContributionCount[]>{
      return this.http.get<EventTypeContributionCount[]>(`${this.apiUrl}/event-types/contribution-count`);
    }

    getCountContributionsByEventAndEventType(eventTypePublicId: string): Observable<ContributionsByEventCount[]>{
      return this.http.get<ContributionsByEventCount[]>(`${this.apiUrl}/count-contributions-by-event/${eventTypePublicId}`);
    }

    getCountContributionsByEventType(): Observable<ContributionCountByEventType[]>{
      return this.http.get<ContributionCountByEventType[]>(`${this.apiUrl}/count-contributions-by-eventtype`);
    }

    downloadPdf(): Observable<Blob> {

      return this.http.get(`${this.apiUrl}/exports/pdf`, {responseType: 'blob'}
      );

    }
}
