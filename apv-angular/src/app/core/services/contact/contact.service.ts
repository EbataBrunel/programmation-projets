import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, catchError, of } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { Contact } from '../../models/Contact';
import { ContactGroupByDate } from '../../models/ContactBroupByDate';
import { UpdateContactStatusRequest } from '../../models/UpdateContactStatusRequest';

@Injectable({
  providedIn: 'root'
})
export class ContactService {

  private apiUrl = `${environment.apiUrl}/contacts`;

  constructor(private http: HttpClient) { }

  getContacts(): Observable<ContactGroupByDate[]> {
    return this.http.get<ContactGroupByDate[]>(`${this.apiUrl}/grouped`).pipe(
      catchError(error => {
        console.error('Erreur API contacts', error);
        return of([]); // empêche Angular de planter
      })
    );
  }

  getContact(publicId: string): Observable<Contact> {
    return this.http.get<Contact>(`${this.apiUrl}/contact/${publicId}`);
  }

  addContact(contact: Contact): Observable<Contact> {
    return this.http.post<Contact>(`${this.apiUrl}`, contact);
  }

  updateStatus(publicId: string, updateContact: UpdateContactStatusRequest) {
    return this.http.patch(`${this.apiUrl}/${publicId}/update-status`, updateContact);
  }

  updateAllStatus(): Observable<number> {
    return this.http.patch<number>(`${this.apiUrl}/status/update-all`, {});
  }

  getCountContactStatus(status: number) {
    return this.http.get<number>(`${this.apiUrl}/count/status/${status}`);
  }

  deleteContact(publicId: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${publicId}`);
  }
}
