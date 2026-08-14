import { Component } from '@angular/core';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-logout',
  templateUrl: './logout.component.html',
  styles: [
  ]
})
export class LogoutComponent {
  constructor(private auth: AuthService, private router: Router){}
  ngOnInit() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
