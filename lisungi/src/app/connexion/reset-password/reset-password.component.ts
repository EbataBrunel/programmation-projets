import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { ActivatedRoute } from '@angular/router';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styles: [
  ]
})
export class ResetPasswordComponent {

  resetForm!: FormGroup;
  token: string | null = null;
  message = '';
  resetPassword: any;

  setting$ = this.settingService.setting$;

  constructor(
    private fb: FormBuilder,
    private titleService: Title,
    private authService: AuthService,
    private settingService: SettingService,
    private route: ActivatedRoute
  ) {
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Reinitialisation | ${setting.nameApp}`);
      }
    });
  }

  initForm(){
    this.resetForm = this.fb.group({
      newPassword: [
        '',
        [
          Validators.required,
          Validators.minLength(8),
          Validators.pattern(/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$/)
        ]
      ],
      confirmPassword: [
        '',
        [
          Validators.required,
          Validators.minLength(8),
          Validators.pattern(/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$/)
        ]
      ]
    });
  }

  ngOnInit() {
    this.initForm();
    this.token = this.route.snapshot.queryParamMap.get('token');
  }

  submit() {
    if (this.resetForm.invalid || !this.token) {
      return;
    }

    if (this.resetForm.value.newPassword !== this.resetForm.value.confirmPassword) {
      this.message = "Les mots de passe ne correspondent pas";
      return;
    }

    this.resetPassword = {
      "token": this.token,
      "password": this.resetForm.value.newPassword
    }

    this.authService.resetPassword(this.resetPassword).subscribe({
      next: (response) => {
        console.log(response);
        this.message = 'Mot de passe mis à jour';
      },
      error: (err) => {
        console.log(err);
        this.message = 'Lien invalide ou expiré';
      }
    });
  }

}
