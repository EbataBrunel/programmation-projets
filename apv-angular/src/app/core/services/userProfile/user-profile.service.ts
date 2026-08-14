import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { UserProfile } from '../../models/UserProfile';
import { UserProfileReasonRemoval } from '../../models/UserProfileReasonRemoval';
import { GenderCount } from '../../models/GenderCount';
import { Reason } from '../../models/Reason';

@Injectable({
  providedIn: 'root'
})
export class UserProfileService {

      private readonly apiUrl = `${environment.apiUrl}/profiles`;

      private profileSubject = new BehaviorSubject<any>(null); // Stocke une valeur qui sera dispobnible àà tous les abonnés

      profile$ = this.profileSubject.asObservable(); // notifier automatiquement tous les composants abonnés quand la valeur change

      constructor(private http: HttpClient) { }

      setProfile(profile: any) {
        this.profileSubject.next(profile);
      }

      getUserProfiles(): Observable<UserProfile[]> {
        return this.http.get<UserProfile[]>(this.apiUrl);
      }

      updateUserProfile(profile: UserProfile): Observable<UserProfile> {
        return this.http.patch<UserProfile>(`${this.apiUrl}/${profile.publicId}`, profile);
      }

      updateUserPhoto(publicId: string, formData: FormData): Observable<UserProfile> {
          return this.http.patch<UserProfile>(
            `${this.apiUrl}/photo/${publicId}`,
            formData
          );
      }

      updateReasonRemoval(publicId: string, userProfileReasonRemoval: UserProfileReasonRemoval): Observable<UserProfile> {
        return this.http.patch<UserProfile>(
          `${this.apiUrl}/reason-removal/${publicId}`,
          userProfileReasonRemoval
        );
      }

      getProfilesByReasonRemovalNot(): Observable<UserProfile[]> {
        return this.http.get<UserProfile[]>(
          `${this.apiUrl}/profile-by-reason-removal`
        );
      }

      deleteUserProfile(publicId: string): Observable<any> {
        return this.http.delete(`${this.apiUrl}/${publicId}`);
      }

      getUserProfile(publicId: string): Observable<UserProfile> {
        return this.http.get<UserProfile>(`${this.apiUrl}/${publicId}`);
      }

      getProfileByUser(userPublicId: string): Observable<UserProfile> {
        return this.http.get<UserProfile>(`${this.apiUrl}/user/${userPublicId}`);
      }

      getTodayRegistrations(){
        return this.http.get<UserProfile[]>(`${this.apiUrl}/today`);
      }

      countProfilesByGender() {
        return this.http.get<GenderCount[]>(
          `${this.apiUrl}/count-by-gender`
        );
      }
}
