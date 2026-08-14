import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Title } from '@angular/platform-browser';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
declare var $: any;


@Component({
  selector: 'app-setting',
  templateUrl: './setting.component.html',
  styles: [
  ]
})
export class SettingComponent {

  settingForm!: FormGroup;
  selectedFile!: File;
  currentSettingId: number | null = null;
  logoPreview: string | null = null;
  errorMessage!: string;

  statusInfo = true;

  themes: string[] = [
    "bg-primary", "bg-success", "bg-info", "bg-danger", "bg-warning", "bg-black", "bg-gray", "bg-navy", "bg-teal", "bg-purple", "bg-orange", "bg-maroon", "bg-white"
  ];

  bodyThemes: string[] = [
    "bg-primary", "bg-success", "bg-info", "bg-danger", "bg-warning", "bg-black", "bg-gray", "bg-navy", "bg-teal", "bg-purple", "bg-orange", "bg-maroon", "bg-white"
  ];

  textColors: string[] = [
    "text-white", "text-primary", "text-success", "text-info", "text-danger", "text-warning", "text-black", "text-gray", "text-navy", "text-teal", "text-purple", "text-orange", "text-maroon"
  ];

  isAdmin$ = this.authService.isAdmin$;

  constructor(
    private fb: FormBuilder,
    private titleService: Title,
    private settingService: SettingService,
    private authService: AuthService
  ) {
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Paramètre | ${setting.nameApp}`);
      }
    });
  }

  ngOnInit(): void {
    this.initForm();
    this.fetchSetting();
  }

  private showModal(id: string) {
    $('#' + id).modal('show');
  }

  initForm() {
    this.settingForm = this.fb.group({
      nameApp: ['', Validators.required],
      nameDev: ['', Validators.required],
      version: ['', Validators.required],
      theme: [null, Validators.required],
      bodyTheme: [null, Validators.required],
      textColor: [null, Validators.required],
      currency: ['', Validators.required],
      address: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      phone: ['', Validators.required],
      width: [0, Validators.required],
      height: [0, Validators.required]
    });
  }

  fetchSetting() {

    this.settingService.loadSetting().subscribe({
      next: (setting) => {
        this.currentSettingId = setting.publicId!;

        this.settingForm.patchValue(setting);
        this.logoPreview = setting.logo;
      },
      error: err => {
        console.error('Impossible de charger le setting', err);
      }
    });
  }

  onFileSelected(event: any) {
    if (event.target.files.length > 0) {
      this.selectedFile = event.target.files[0];

      const reader = new FileReader();
      reader.onload = () => {
        this.logoPreview = reader.result as string;
      };
      reader.readAsDataURL(this.selectedFile);
    }
  }

  submit() {

    if (!this.authService.isAdmin()) {
      this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
      return;
    }

    if (this.settingForm.invalid) {
        this.settingForm.markAllAsTouched();
        return;
    }

    const formData = new FormData();

    formData.append(
      'data',
      new Blob([JSON.stringify(this.settingForm.value)], { type: 'application/json' })
    );

    if (this.selectedFile) {
      formData.append('logo', this.selectedFile);
    }

    if (this.currentSettingId) {
      // UPDATE
      this.settingService.updateSetting(this.currentSettingId, formData).subscribe({
        next: (settingUpdate) => {
          this.logoPreview = settingUpdate.logo;
          this.statusInfo = false;
          this.showModal('infoModal');
        },
        error: (err) => console.error(err)
      });
    } else {
      // CREATE
      this.settingService.addSetting(formData).subscribe({
        next: (setting) => {
          this.currentSettingId = setting.publicId!;
          this.logoPreview = setting.logo;
          this.statusInfo = true;
          this.showModal('infoModal');
        },
        error: (err) => console.error(err)
      });
    }
  }
}
