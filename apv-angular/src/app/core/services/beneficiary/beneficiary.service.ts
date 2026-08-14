import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { Beneficiary } from '../../models/Beneficiary';

@Injectable({
  providedIn: 'root'
})
export class BeneficiaryService {

  private readonly apiUrl = `${environment.apiUrl}/beneficiaries`;

  constructor(private readonly http: HttpClient) {}

  getBeneficiaries(): Observable<Beneficiary[]> {
    return this.http.get<Beneficiary[]>(this.apiUrl);
  }

  getBeneficiaryByPublicId(publicId: string): Observable<Beneficiary> {
    return this.http.get<Beneficiary>(`${this.apiUrl}/${publicId}`);
  }

  addBeneficiary(formData: FormData): Observable<Beneficiary> {
    return this.http.post<Beneficiary>(this.apiUrl, formData);
  }

  updateBeneficiary(publicId: string, formData: FormData): Observable<Beneficiary> {
    return this.http.patch<Beneficiary>(
      `${this.apiUrl}/${publicId}`,
      formData
    );
  }

  deleteBeneficiary(publicId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${publicId}`);
  }
}
