import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { RegulationService } from 'src/app/core/services/regulation/regulation.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { Regulation } from 'src/app/core/models/Regulation';
import { Title } from '@angular/platform-browser';

declare var $: any;

@Component({
  selector: 'app-regulation',
  templateUrl: './regulation.component.html',
  styles: [
  ]
})
export class RegulationComponent {
      regulations: Regulation[] = [];
      regulationNames: string[] = [];

      error!: string;
      errorMessage = '';
      selectedRegulation!: Regulation;

      RegulationName!: string;
      publicId!: string;

      regulationForm!: FormGroup;
      statusInfo = true;

      setting$ = this.settingService.setting$;
      isAdmin$ = this.authService.isAdmin$;

      constructor(
        private fb: FormBuilder,
        private titleService: Title,
        private regulationService: RegulationService,
        private settingService: SettingService,
        private authService: AuthService
      ) {
        this.settingService.setting$.subscribe(setting => {
          if (setting?.nameApp) {
            this.titleService.setTitle(`Règlements | ${setting.nameApp}`);
          }
        });
      }

      ngOnInit(): void {
        this.initForm();
        this.fetchRegulations();
        this.getRegulationNames();
      }

      initForm() {

        this.regulationForm = this.fb.group({
          name: [null, Validators.required],
          description: ['', Validators.required]

        });
      }

      private showModal(id: string) {
        $('#' + id).modal('show');
      }

      private hideModal(id: string) {
        $('#' + id).modal('hide');
      }

      getRegulationNames(){
        for (let i = 1; i <= 30; i++) {
          this.regulationNames.push(`Regle ${i}`);
        }
      }

      openDeleteModal(regulation: any) {
        this.selectedRegulation = regulation;
        this.showModal('deleteModal');
      }

      deleteRegulation(publicId: string){

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        this.regulationService.deleteRegulation(publicId).subscribe({
          next: () =>{
            this.hideModal('deleteModal');
            this.fetchRegulations();
          },
          error: err => this.error = err.message
        });
      }

      fetchRegulations(): void {

        this.regulationService.getRegulations().subscribe({
          next: (data) => {
            this.regulations = data;
          },
          error: err => this.error = err.message
        });
      }

      openAddModal(){
        this.errorMessage = '';
        this.initForm();
        this.showModal('addRegulationModal');
      }

      addRegulation(){

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        this.errorMessage = '';
        const formData = new FormData();

        formData.append(
          'data',
          new Blob([JSON.stringify(this.regulationForm.value)], { type: 'application/json' })
        );

        this.regulationService.addRegulation(formData).subscribe({
          next: () => {
            this.initForm();
            this.statusInfo = true;
            this.fetchRegulations();
            this.showModal('infoModal');
          },
          error: (err) => {
            console.log(err);
            this.errorMessage = err.error;
          }
        });
      }

      openUpdateModal(id: any){

        this.errorMessage = '';

        this.regulationService.getRegulation(id).subscribe({
          next: (data) => {
            this.publicId = data.publicId!;

            this.regulationForm = this.fb.group({
              name: data.name,
              description: data.description
            });

            this.showModal('updateRegulationModal');
          },
          error: err => this.error = err.message
        })
      }

      updRegulation() {

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        this.errorMessage = '';

        const formData = new FormData();

        formData.append(
          'data',
          new Blob([JSON.stringify(this.regulationForm.value)], { type: 'application/json' })
        );
        this.regulationService.updateRegulation(this.publicId, formData).subscribe({
          next: () => {
            this.statusInfo = false;
            this.fetchRegulations();
            this.showModal('infoModal');
          },
          error: (err) => {
            console.log(err);
            this.errorMessage = err.error;
          }
        });
      }
}
