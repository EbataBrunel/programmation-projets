import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { Donation } from '../../models/Donation';
import { BeneficiaryCount } from '../../models/BeneficiaryCount';
import { DonationCountByYear } from '../../models/DonationCountByYear';

@Injectable({
  providedIn: 'root'
})
export class DonationService {

  private readonly apiUrl = `${environment.apiUrl}/donations`;

  constructor(private http: HttpClient) { }

  getDonations(): Observable<Donation[]> {
    return this.http.get<Donation[]>(this.apiUrl);
  }

  addDonation(formData: FormData): Observable<Donation> {
    return this.http.post<Donation>(this.apiUrl, formData);
  }

  getCountDonationsByBeneficiary(): Observable<BeneficiaryCount[]>{
    return this.http.get<BeneficiaryCount[]>(`${this.apiUrl}/count/donation`);
  }

  findDonationsBybenecifiaryId(beneficiaryId: number): Observable<Donation[]>{
    return this.http.get<Donation[]>(`${this.apiUrl}/donations/${beneficiaryId}`);
  }

  updateVisibilityDoanation(publicId: string): Observable<Donation> {
    return this.http.patch<Donation>(
        `${this.apiUrl}/update-visibility/${publicId}`,
        {}
    );
  }


  updateClosureStatusDoantion(publicId: string, data: any): Observable<Donation> {
    return this.http.patch<Donation>(
        `${this.apiUrl}/update-closure-status/${publicId}`,
        data
    );
  }

  updateDonation(publicId: string, formData: FormData): Observable<Donation> {
    return this.http.patch<Donation>(
      `${this.apiUrl}/${publicId}`,
      formData
    );
  }

  deleteDonation(publicId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${publicId}`);
  }

  getDonation(publicId: string): Observable<Donation> {
    return this.http.get<Donation>(`${this.apiUrl}/${publicId}`);
  }

  getDonationById(id: number): Observable<Donation> {
    return this.http.get<Donation>(`${this.apiUrl}/id/${id}`);
  }

  getDonationsByYear(year: number): Observable<Donation[]> {

        const params = new HttpParams()
          .set('year', year);

        return this.http.get<Donation[]>(
          `${this.apiUrl}/year`,
          { params }
        );
      }

  getDonationsByMonth(year: number, month: number): Observable<Donation[]> {

        const params = new HttpParams()
          .set('year', year)
          .set('month', month);

        return this.http.get<Donation[]>(
          `${this.apiUrl}/month`,
          { params }
        );
  }

  countDonationsByYear(): Observable<DonationCountByYear[]> {
    return this.http.get<DonationCountByYear[]>(
          `${this.apiUrl}/statistics/by-year`
    );
  }
}
