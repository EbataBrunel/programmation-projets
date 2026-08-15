import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { Setting } from 'src/app/core/models/Setting';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styles: [
  ]
})
export class ForgotPasswordComponent {

  forgotForm: FormGroup;
  message = '';
  request : any

  setting$ = this.settingService.setting$;

  constructor(
    private fb: FormBuilder,
    private titleService: Title,
    private authService: AuthService,
    private settingService: SettingService
  ) {
    this.forgotForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]]
    });

    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Mot de passe oublié | ${setting.nameApp}`);
      }
    });
  }


  ngOnInit() {

  }


  submit() {
    if (this.forgotForm.invalid) {
      return;
    }

    this.request = {
      "email": this.forgotForm.value.email
    }

    this.authService.forgotPassword(this.request)
      .subscribe({
        next: () => {
          this.message = 'Un email de réinitialisation a été envoyé.';
        },
        error: () => {
          this.message = 'Si l’email existe, un lien a été envoyé.';
        }
      });
  }
}
