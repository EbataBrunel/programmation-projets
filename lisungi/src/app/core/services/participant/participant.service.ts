import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { DonationParticipant } from '../../models/DonationParticipant';
import { ParticipantsByDonationCount } from '../../models/ParticipantsByDonationCount';
import { BeneficiaryDonationParticipantCount } from '../../models/BeneficiaryDonationParticipantCount';

@Injectable({
  providedIn: 'root'
})
export class ParticipantService {

    private readonly apiUrl = `${environment.apiUrl}/donation-participants`;

    constructor(private http: HttpClient) { }

    getDonationParticipants(): Observable<DonationParticipant[]> {
      return this.http.get<DonationParticipant[]>(this.apiUrl);
    }

    addDonationParticipant(formData: FormData): Observable<DonationParticipant> {
      return this.http.post<DonationParticipant>(this.apiUrl, formData);
    }

    updateDonationParticipant(publicId: string, formData: FormData): Observable<DonationParticipant> {
      return this.http.patch<DonationParticipant>(
        `${this.apiUrl}/${publicId}`,
        formData
      );
    }

    deleteDonationParticipant(publicId: string): Observable<void> {
      return this.http.delete<void>(`${this.apiUrl}/${publicId}`);
    }

    getDonationParticipant(publicId: string): Observable<DonationParticipant> {
      return this.http.get<DonationParticipant>(`${this.apiUrl}/${publicId}`);
    }

    getParticipantsByDonation(publicId: string): Observable<DonationParticipant[]> {
        return this.http.get<DonationParticipant[]>(`${this.apiUrl}/donation/${publicId}`);
    }

    getCountDonationByBeneficiaryWithParticipant(): Observable<BeneficiaryDonationParticipantCount[]>{
      return this.http.get<BeneficiaryDonationParticipantCount[]>(`${this.apiUrl}/beneficiaries/donation-participant-count`);
    }

    getCountParticipantsByDonationAndBeneficiary(beneficiaryPublicId: string): Observable<ParticipantsByDonationCount[]>{
      return this.http.get<ParticipantsByDonationCount[]>(`${this.apiUrl}/count-participant-by-donation/${beneficiaryPublicId}`);
    }
}
