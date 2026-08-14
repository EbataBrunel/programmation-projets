import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { User } from '../../models/User';
import { Role } from '../../models/Role';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private apiUrl = `${environment.apiUrl}/users`;

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.apiUrl}`);
  }

  postUser(user: User): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}`, user);
  }

  getUser(publicId: string): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${publicId}`);
  }

  getUserById(userId: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/id/${userId}`);
  }

  getUserByUsername(username: string): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/get/${username}`);
  }

  getAllRoles(): Observable<Role[]> {
    return this.http.get<Role[]>(`${this.apiUrl}/roles`);
  }

  addRoleToUser(userPublicId: string, roleName: string): Observable<User> {
    return this.http.post<User>(
      `${this.apiUrl}/${userPublicId}/roles/${roleName}`,
      {}
    );
  }

  removeRoleToUser(userPublicId: string, roleName: string): Observable<User> {
    return this.http.delete<User>(
      `${this.apiUrl}/${userPublicId}/roles/${roleName}`
    );
  }

  deleteUser(userId: string): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}/${userId}`
    );
  }
}
