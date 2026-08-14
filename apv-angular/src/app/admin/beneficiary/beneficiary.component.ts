import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { Title } from '@angular/platform-browser';
import { BeneficiaryService } from 'src/app/core/services/beneficiary/beneficiary.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { Beneficiary } from 'src/app/core/models/Beneficiary';
import { DATATABLE_FR } from 'src/app/core/config/datatable-fr';
import { AuthService } from 'src/app/core/services/authentication/auth.service';

declare var $: any;

@Component({
  selector: 'app-beneficiary',
  templateUrl: './beneficiary.component.html',
  styles: [
  ]
})
export class BeneficiaryComponent {
    beneficiaries: Beneficiary[] = [];
    types: String[] = [
      "PARTICULIER",
      "ORPHELINAT",
      "ASSOCIATION",
      "EGLISE",
      "ECOLE",
      "ONG",
      "AUTRE"
    ]

    selectedBeneficiary!: Beneficiary;
    error: string = '';
    errorMessage = '';
    logoUrl= '';

    publicId: any;
    statusInfo = true;

    beneficiaryForm!: FormGroup;

    setting$ = this.settingService.setting$;
    isAdmin$ = this.authService.isAdmin$;

    constructor(
      private fb: FormBuilder,
      private titleService: Title,
      private beneficiaryService: BeneficiaryService,
      private settingService: SettingService,
      private authService: AuthService
    ) {
      this.settingService.setting$.subscribe(setting => {
        if (setting?.nameApp) {
          this.titleService.setTitle(`Bénéficiaires | ${setting.nameApp}`);
        }
      });
    }

    ngOnInit(): void {
      this.initForm();
      this.fetchBeneficiaries();
    }

    initForm() {
      this.beneficiaryForm = this.fb.group({
            name: ['', Validators.required],
            country: ['', Validators.required],
            city: ['', Validators.required],
            borough: ['', Validators.required],
            address: ['', Validators.required],
            email: [''],
            phone: [''],
            type: [null, Validators.required],
            dateExistence: [new Date(), Validators.required]

      });
    }

    private showModal(id: string) {
      $('#' + id).modal('show');
    }

    private hideModal(id: string) {
      $('#' + id).modal('hide');
    }

    openDetailModal(beneficiary: Beneficiary){
      this.selectedBeneficiary = beneficiary;
      this.showModal('detailModal');
    }

    openDeleteModal(beneficiary: Beneficiary) {
        this.selectedBeneficiary = beneficiary;
        this.showModal('deleteModal');
    }

    deleteBeneficiary(publicId:any){

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }

      this.beneficiaryService.deleteBeneficiary(publicId).subscribe({
        next: () => {
          this.fetchBeneficiaries();
          this.hideModal('deleteModal');
        },
        error: err => this.error = err.message
      });
    }

    fetchBeneficiaries(): void {

      if ($.fn.DataTable.isDataTable('#example1')) {
        $('#example1').DataTable().destroy();
      }

      this.beneficiaryService.getBeneficiaries().subscribe({
        next: (data) => {
          this.beneficiaries = data;

          setTimeout(() => {
            $('#example1').DataTable({
              language: DATATABLE_FR,
              destroy: true
            });
          }, 100);
        },
        error: err => this.error = err.message
      });
    }

    openAddModal(){
      this.errorMessage = '';
      this.initForm();
      this.showModal('addBeneficiaryModal');
    }

    addBeneficiary(){

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }

      const formData = new FormData();

      formData.append(
        'data',
        new Blob([JSON.stringify(this.beneficiaryForm.value)], { type: 'application/json' })
      );

      this.beneficiaryService.addBeneficiary(formData).subscribe({
        next: () => {
          this.initForm();
          this.statusInfo = true;
          this.fetchBeneficiaries();
          this.showModal('infoModal');
        },
        error: (err) => {
          console.log(err);
          this.errorMessage = err.error;
        }
      });
    }

    openUpdateModal(publicId: string){

      this.errorMessage = '';

      this.beneficiaryService.getBeneficiaryByPublicId(publicId).subscribe({
        next: (data) => {
          this.publicId = data.publicId!;

          this.beneficiaryForm = this.fb.group({
              type:data.type,
              name: data.name,
              country: data.country,
              city: data.city,
              borough: data.borough,
              address: data.address,
              email: data.email,
              phone: data.phone,
              dateExistence: data.dateExistence
          });

          this.showModal('updateBeneficiaryModal');
        },
        error: err => this.error = err.message
      })
    }

    updBeneficiary() {

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }

      const formData = new FormData();

      formData.append(
        'data',
        new Blob([JSON.stringify(this.beneficiaryForm.value)], { type: 'application/json' })
      );

      this.beneficiaryService.updateBeneficiary(this.publicId, formData).subscribe({
        next: () => {
          this.statusInfo = false;
          this.fetchBeneficiaries();
          this.showModal('infoModal');
        },
        error: (err) => {
          console.log(err);
          this.errorMessage = err.error;
        }
      });
    }
}
