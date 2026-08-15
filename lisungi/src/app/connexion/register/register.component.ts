import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Title } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { Setting } from 'src/app/core/models/Setting';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styles: [
  ]
})
export class RegisterComponent {

  setting!: Setting;
  registerData = {
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  };

  loginData = {
    username: '',
    password: ''
  };

  loginError = '';
  loginSuccess = '';

  errorMessage = '';
  successMessage = '';

  setting$ = this.settingService.setting$;

  constructor(
    private titleService: Title,
    private authService: AuthService,
    private settingService: SettingService,
    private router: Router
  ) {
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Inscription| ${setting.nameApp}`);
      }
    });
  }

  register(form: NgForm) {

    if (form.invalid) return;

    if (this.registerData.password !== this.registerData.confirmPassword) {
      this.errorMessage = "Les mots de passe ne correspondent pas";
      return;
    }

    this.authService.register(this.registerData).subscribe({
      next: (response) => {

        // Si ton backend renvoie un token
        if (response.token) {
          localStorage.setItem('token', response.token);
        }

        this.successMessage = "Inscription réussie";

        setTimeout(() => {
          this.router.navigate(['/register']);
        }, 1500);
      },
      error: (err) => {
        this.errorMessage = err.error?.message || "Erreur lors de l'inscription";
      }
    });
  }
}
