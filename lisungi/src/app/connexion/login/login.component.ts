import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Title } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { UserService } from 'src/app/core/services/user/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styles: [
  ]
})
export class LoginComponent {

  form!: FormGroup;
  errorMessage = '';

  setting$ = this.settingService.setting$;

  constructor(
    private fb: FormBuilder,
    private titleService: Title,
    private authService: AuthService,
    private settingService: SettingService,
    private userService: UserService,
    private router: Router
  ) {
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Login | ${setting.nameApp}`);
      }
    });
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  login(): void {
    if (this.form.invalid) return;

    this.authService.login(this.form.value).subscribe({
      next: res => {
        localStorage.setItem('token', res.token);

        this.authService.setRoles(res.roles);

        this.userService.getUserByUsername(res.username).subscribe({
          next: (user) => {
            this.authService.setCurrentUser(user);
            this.router.navigate(['/dashboard']);
          },
          error: (err) => console.error(err)
        })
      },
      error: () => {
        this.errorMessage = 'Nom d’utilisateur ou mot de passe incorrect';
      }
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
