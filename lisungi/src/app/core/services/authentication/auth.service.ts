import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, map } from 'rxjs';
import { environment } from 'src/app/environments/environment';
import { RegisterRequest } from '../../models/RegisterRequest';
import { AuthResponse } from '../../models/AuthResponse';
import { ForgotPasswordRequest } from '../../models/ForgotPasswordRequest';
import { ResetPasswordRequest } from '../../models/ResetPasswordRequest';
import { ChangePasswordRequest } from '../../models/ChangePasswordRequest';
import { MessageResponse } from '../../models/MessageResponse';
import { User } from '../../models/User';
import { UserService } from '../user/user.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = `${environment.apiUrl}/auth`;

  private rolesSubject = new BehaviorSubject<string[]>(this.getStoredRoles());

  private currentUserSubject = new BehaviorSubject<User | null>(null);

  public currentUser$: Observable<User | null> = this.currentUserSubject.asObservable();

  roles$ = this.rolesSubject.asObservable();

  isAdmin$ = this.roles$.pipe(
    map(roles =>
      roles.includes('ROLE_ADMIN') ||
      roles.includes('ROLE_SUPADMIN')
    )
  );

  isSupAdmin$ = this.roles$.pipe(
    map(roles =>
      roles.includes('ROLE_SUPADMIN')
    )
  );


  constructor(
    private http: HttpClient,
    private userService: UserService
  ) {}

  private getStoredRoles(): string[] {

    const storedRoles = localStorage.getItem('roles');

    if (!storedRoles) {
      return [];
    }

    try {
      return JSON.parse(storedRoles);
    } catch {
      return [];
    }
  }

  setRoles(roles: string[]): void {
    localStorage.setItem('roles', JSON.stringify(roles));
    this.rolesSubject.next(roles);
  }


  getRoles(): string[] {
    return this.rolesSubject.value;
  }

  isAdmin(): boolean {
    const roles = this.rolesSubject.value;

    return roles.includes('ROLE_ADMIN') ||
           roles.includes('ROLE_SUPADMIN');
  }

  isSupAdmin(): boolean {
    return this.rolesSubject.value.includes('ROLE_SUPADMIN');
  }

  /** * Met à jour l'utilisateur connecté */
  setCurrentUser(user: User | null): void {
    this.currentUserSubject.next(user);
  }
  /** * Récupère l'utilisateur actuellement connecté */
  getCurrentUsr(): User | null {
    return this.currentUserSubject.value;
  }


  register(data: RegisterRequest): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, data);
  }

  /** Récuperer l'utilisateur connecté depuis le backend */
  getCurrentUser() {
    return this.http.get<AuthResponse>(`${this.apiUrl}/me`);
  }

   /**
   * Restaure l'utilisateur après
   * un refresh de la page
   */
  restoreCurrentUser(): void {

    const token = this.getToken();

    if (!token) {
      this.currentUserSubject.next(null);
      return;
    }

    this.getCurrentUser().subscribe({
      next: (usr) => {

        console.log(
          'Utilisateur restauré :',
          usr
        );

        this.userService.getUserByUsername(usr.userName).subscribe({
          next: (user) => {
            this.currentUserSubject.next(user);

            // On peut également restaurer
            // les rôles depuis l'utilisateur
            if (user.roles) {

              const roles = user.roles.map(
                role => role.name
              );

              this.setRoles(roles);
            }
          },
          error: (err) => console.error(err)
        });
      },

      error: (error) => {

        console.error(
          'Impossible de restaurer l’utilisateur :',
          error
        );

        this.currentUserSubject.next(null);

        // Si le JWT n'est plus valide
        if (error.status === 401) {

          localStorage.removeItem('token');
          localStorage.removeItem('roles');

          this.rolesSubject.next([]);
        }
      }
    });
  }

  login(data:any) {
    return this.http.post<any>(`${this.apiUrl}/login`, data);
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('roles');
    this.currentUserSubject.next(null);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  getUsernameFromToken(): string | null {
    const token = localStorage.getItem('token');
    if (!token) return null;

    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.sub;
  }

  forgotPassword(request: ForgotPasswordRequest): Observable<MessageResponse> {
    return this.http.post<MessageResponse>(`${this.apiUrl}/forgot-password`, request);
  }

  resetPassword(request: ResetPasswordRequest): Observable<MessageResponse> {
    return this.http.post<MessageResponse>(`${this.apiUrl}/reset-password`, request);
  }

  changePassword(request: ChangePasswordRequest) {
    return this.http.put(`${this.apiUrl}/change-password`, request);
  }
}
