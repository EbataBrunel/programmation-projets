import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { switchMap } from 'rxjs';
import { ParticipantService } from 'src/app/core/services/participant/participant.service';
import { DonationService } from 'src/app/core/services/donation/donation.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { Donation } from 'src/app/core/models/Donation';
import { DonationParticipant } from 'src/app/core/models/DonationParticipant';
import { BeneficiaryCount } from 'src/app/core/models/BeneficiaryCount';
import { ParticipantsByDonationCount } from 'src/app/core/models/ParticipantsByDonationCount';
import { BeneficiaryDonationParticipantCount } from 'src/app/core/models/BeneficiaryDonationParticipantCount';
import { DATATABLE_FR } from 'src/app/core/config/datatable-fr';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { Title } from '@angular/platform-browser';

declare var $: any;

@Component({
  selector: 'app-donation-participant',
  templateUrl: './donation-participant.component.html',
  styles: [
  ]
})
export class DonationParticipantComponent {
      countDonationByBeneficiary: BeneficiaryDonationParticipantCount[] = [];
      beneficiariesCount: BeneficiaryCount[] = [];
      donationParticipants: DonationParticipant[] = [];
      donations: Donation[] = []
      //beneficiaries: Beneficiary[] = [];
      participantsDonation: ParticipantsByDonationCount[] = [];
      itemType: String[] = [
          "PARTICULIER",
          "ENTREPRISE",
          "ASSOCIATION",
          "FOUNDATION",
          "GOUVERNEMENT",
          "AUTRE"
      ]

      error: string = '';
      errorMessage!: string;
      selectedParticipantDonation!: DonationParticipant;

      beneficiaryName!: string;
      donationTitle!: string;

      beneficiaryId: number | null = null;

      publicId: any;
      statusInfo = true;
      submitted = false;

      currentDonationPublicId!: string;
      currentDonationTitle!: string;
      currentBneficiaryPublicId!: string;
      currentBeneficiaryName!: string;
      closure_status!: boolean;

      participantForm!: FormGroup;

       setting$ = this.settingService.setting$;
       isAdmin$ = this.authService.isAdmin$;

      constructor(
          private fb: FormBuilder,
          private titleService: Title,
          private participationService: ParticipantService,
          private donationService: DonationService,
          private settingService: SettingService,
          private authService: AuthService
      ) {
        this.settingService.setting$.subscribe(setting => {
          if (setting?.nameApp) {
            this.titleService.setTitle(`participants | ${setting.nameApp}`);
          }
        });
      }

      ngOnInit(): void {
          this.initForm();
          this.fetchBeneficiaries();
          this.getBeneficiaries();
      }

      initForm() {
        this.beneficiaryId = null;

        this.participantForm = this.fb.group({
            name: ['', Validators.required],
            amount: [null],
            description: [''],
            itemType: [null, Validators.required],
            donationId: [null, Validators.required],

        });
      }

      private showModal(id: string) {
        $('#' + id).modal('show');
      }

      private hideModal(id: string) {
        $('#' + id).modal('hide');
      }

      getBeneficiaries(){
          this.donationService.getCountDonationsByBeneficiary().subscribe({
            next: (data) => this.beneficiariesCount = data,
            error: (err) => console.log(err)
          });
      }

      fetchBeneficiaries(): void {

          if ($.fn.DataTable.isDataTable('#example1')) {
            $('#example1').DataTable().destroy();
          }

          this.participationService.getCountDonationByBeneficiaryWithParticipant().subscribe({
            next: (data) => {
              this.countDonationByBeneficiary = data;

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

      onBeneficiaryChange(event: Event) {

          const value = (event.target as HTMLSelectElement).value;

          // Réinitialiser le select des événements
          this.participantForm.get('donationId')?.reset();

          if (value !== null) {
            this.beneficiaryId = Number(value);
            this.donationService.findDonationsBybenecifiaryId(this.beneficiaryId).subscribe({
              next: (data) => {
                this.donations = data.filter(donation => donation.closure_status === false);
              },
              error: (err) => console.log(err)
            });
          }else {
            this.beneficiaryId = null;
            this.donations = [];
            this.submitted = false;
          }

      }

      /*
       onBeneficiaryTypeChange(event: Event){
        const value = (event.target as HTMLSelectElement).value;

       }*/

      openModalDonations(beneficiaryPublicId: string, beneficiaryName: string){


        this.currentBneficiaryPublicId = beneficiaryPublicId;
        this.currentBeneficiaryName = beneficiaryName;

        this.loadDonations();
      }

      loadDonations(){
        this.beneficiaryName = this.currentBeneficiaryName;

        if ($.fn.DataTable.isDataTable('#donationsTable')) {
            $('#donationsTable').DataTable().destroy();
        }

        this.participationService.getCountParticipantsByDonationAndBeneficiary(this.currentBneficiaryPublicId).subscribe({
            next: (data) => {
              this.participantsDonation = data;
              this.showModal('DonationsModal');
              setTimeout(() => {

                $('#donationsTable').DataTable({
                  language: DATATABLE_FR,
                  destroy: true
                });

              }, 300);
            },
            error: (err) => console.log(err)
        });

      }

      openDonationParticipantModal(donationPublicId: string, donationTitle: string, closure_status: boolean){

          this.currentDonationPublicId = donationPublicId;
          this.currentDonationTitle = donationTitle;
          this.closure_status = closure_status;

          this.loadDonationParticipants();
      }

      loadDonationParticipants(){

        this.donationTitle = this.currentDonationTitle;

        if ($.fn.DataTable.isDataTable('#donationsTable')) {
            $('#donationsTable').DataTable().destroy();
        }
        this.participationService.getParticipantsByDonation(this.currentDonationPublicId).subscribe({
            next: (data) => {
              this.donationParticipants = data;
              this.showModal('donationParticipantsModal');

              setTimeout(() => {

                $('#participantsTable').DataTable({
                  language: DATATABLE_FR,
                  destroy: true
                });

              }, 300);
            },
            error: (err) => console.log(err)
        });
      }

      openDeleteModal(donationParticipant: any) {
        this.selectedParticipantDonation = donationParticipant;
        this.showModal('deleteModal');
      }

      deleteDonationParticipant(publicId:any){

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        this.participationService.deleteDonationParticipant(publicId).subscribe({
          next: ()=>{
              this.hideModal('deleteModal');

              // Mise à jour du tableau principal
              this.fetchBeneficiaries();

              // Récharger des donnations
              this.loadDonations();

              // Récharger uniquement des participants
              this.loadDonationParticipants();
          }
        });
      }


      openAddModal(){
        this.errorMessage = '';
        this.submitted = false;
        this.initForm();
        this.showModal('addDonationParticipantModal');
      }

      addDonationParticipant(){

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        this.submitted = true;
        this.errorMessage = '';

        if (this.beneficiaryId === null) {
          return;
        }

        const formData = new FormData();

        formData.append(
          'data',
          new Blob([JSON.stringify(this.participantForm.value)], { type: 'application/json' })
        );
        this.participationService.addDonationParticipant(formData).subscribe({
          next: () => {
            this.initForm();
            this.statusInfo = true;
            this.fetchBeneficiaries();
            this.hideModal('addDonationParticipantModal');
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
        this.submitted = false;

        this.participationService.getDonationParticipant(publicId).pipe(
          switchMap(data => {

            this.publicId = data.publicId;

            this.participantForm = this.fb.group({
              name: data.name,
              amount: data.amount,
              itemType: data.itemType,
              description: data.description,
              donationId: data.donationId
            });

            return this.donationService.getDonationById(data.donationId!);
          }),

              switchMap(donation => {

              this.beneficiaryId = donation.beneficiaryId;

              return this.donationService.findDonationsBybenecifiaryId(donation.beneficiaryId!);
            })
        )
        .subscribe({
          next: donations => {
            this.donations = donations.filter(donation => donation.closure_status === true);
            this.showModal('updateDonationParticipantModal');
          },
          error: err => {
                console.log(err);
          }

      });
    }

    updDonationParticipant() {

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }

      this.submitted = true;
      this.errorMessage = '';

      if (this.beneficiaryId === null) {
        return;
      }

      const formData = new FormData();

      formData.append(
        'data',
        new Blob([JSON.stringify(this.participantForm.value)], { type: 'application/json' })
      );

      this.participationService.updateDonationParticipant(this.publicId, formData).subscribe({
        next: () => {
          this.statusInfo = false;
          this.fetchBeneficiaries();
          this.loadDonations();
          this.loadDonationParticipants();
          this.showModal('infoModal');
        },
          error: (err) => {

          console.log(err);

          this.errorMessage = err.error;

        }
      });
    }
}
