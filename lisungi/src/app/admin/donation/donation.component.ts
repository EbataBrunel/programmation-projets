import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { DonationService } from 'src/app/core/services/donation/donation.service';
import { ParticipantService } from 'src/app/core/services/participant/participant.service';
import { BeneficiaryService } from 'src/app/core/services/beneficiary/beneficiary.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { DonationParticipant } from 'src/app/core/models/DonationParticipant';
import { Beneficiary } from 'src/app/core/models/Beneficiary';
import { Donation } from 'src/app/core/models/Donation';
import { BeneficiaryCount } from 'src/app/core/models/BeneficiaryCount';
import { DATATABLE_FR } from 'src/app/core/config/datatable-fr';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { DonationCountByYear } from 'src/app/core/models/DonationCountByYear';
import { Title } from '@angular/platform-browser';

declare var $: any;

@Component({
  selector: 'app-donation',
  templateUrl: './donation.component.html',
  styles: [
  ]
})
export class DonationComponent {
      beneficiariesCount: BeneficiaryCount[] = [];
      donations: Donation[] = [];
      donationsStat: Donation[] = [];
      participants: DonationParticipant[] = [];
      beneficiaries: Beneficiary[] = [];
      donationsByYear: DonationCountByYear[] = [];

      months = [
              { key: 1, value: 'Janvier' },
              { key: 2, value: 'Février' },
              { key: 3, value: 'Mars' },
              { key: 4, value: 'Avril' },
              { key: 5, value: 'Mai' },
              { key: 6, value: 'Juin' },
              { key: 7, value: 'Juillet' },
              { key: 8, value: 'Août' },
              { key: 9, value: 'Septembre' },
              { key: 10, value: 'Octobre' },
              { key: 11, value: 'Novembre' },
              { key: 12, value: 'Décembre' }
      ];

      selectedDonation: Donation |  null = null;

      error: string = '';
      errorMessage = '';

      beneficiaryName!: string;
      titleDonation!: string;
      currentBeneficiaryId!: number;
      currentEvenTypeName!: string;
      captchaToken: string | null = null;

      publicId: any;

      statusInfo = true;

      donationForm!: FormGroup;
      selectedFile!: File;
      photoPreview: string = '';

      year!: number|null;
      month!: number|null;

      setting$ = this.settingService.setting$;
      isAdmin$ = this.authService.isAdmin$;
      isSupAdmin$ = this.authService.isSupAdmin$;

      constructor(
        private fb: FormBuilder,
        private titleService: Title,
        private participantService: ParticipantService,
        private donationService: DonationService,
        private beneficiaryService: BeneficiaryService,
        private settingService: SettingService,
        private authService: AuthService
      ) {
        this.settingService.setting$.subscribe(setting => {
          if (setting?.nameApp) {
            this.titleService.setTitle(`Dons | ${setting.nameApp}`);
          }
        });
      }

      ngOnInit(): void {
        this.initForm();
        this.fetchDonations();
        this.getBeneficiaries();
        this. loadDonationsByYearCount();
      }

      initForm() {
        this.donationForm = this.fb.group({
          title: ['', Validators.required],
          description: ['', Validators.required],
          dateDonation: ['', Validators.required],
          beneficiaryId: [null, Validators.required],

        });
      }

      private showModal(id: string) {
        $('#' + id).modal('show');
      }

      private hideModal(id: string) {
        $('#' + id).modal('hide');
      }


      openDeleteModal(donation: any) {
          this.selectedDonation = donation;
          this.showModal('deleteModal');
      }

      openDetailModal(donation: Donation){
        this.selectedDonation = donation;
        this.showModal('detailModal');
      }

      openVisibilityModal(donation: Donation){
        this.selectedDonation = donation;
        this.showModal('visibilityModal');
      }

      openClosureStatusModal(donation: Donation){
        this.selectedDonation = donation;
        this.showModal('closureStatusModal');
      }

      captchaResolved(token: string | null) {

        this.captchaToken = token;

      }

      openStatDonation(){
        this.year = null;
        this.showModal('statModal');
      }

      onYearChange(event: globalThis.Event) {

          this.month = null;

          const value = (event.target as HTMLSelectElement).value;

          if (value !== null) {

            this.year = Number(value);

            this.loadDonationsByYear(this.year)

          } else {
            this.year = 0;
          }
      }

      onMonthChange(event: globalThis.Event) {

          const value = (event.target as HTMLSelectElement).value;

          if (value !== null) {

            this.month = Number(value);

            this.loadDonationsByMonth(this.year!, this.month!)

          } else {
            this.year = 0;
          }
      }

      loadDonationsByYear(year: number) {

        this.donationService.getDonationsByYear(year)
          .subscribe({
            next: (data) => {
              this.donationsStat = data;
            },
            error: (error) => {
              console.error('Erreur lors du chargement des événements', error);
            }
          });
      }

      loadDonationsByMonth(year: number, month: number) {

        this.donationService.getDonationsByMonth(year, month)
          .subscribe({
            next: (data) => {
              this.donationsStat = data;
            },
            error: (error) => {
              console.error('Erreur lors du chargement des événements', error);
            }
          });
      }

      loadDonationsByYearCount() {
        this.donationService.countDonationsByYear().subscribe({
          next: (data) => {
            this.donationsByYear = data;
          },
          error: (error) => {
            console.error(
              'Erreur lors du chargement des statistiques',
              error
            );
          }
        });
      }


      deleteDonation(publicId:any){

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        this.donationService.deleteDonation(publicId).subscribe({
          next: () =>{
              this.fetchDonations();

              // Mise à jour du tableau principal
              this.fetchDonations();

              // Rchargement les dons
              this.loadDonations();
              this.hideModal('deleteModal');
          },
          error: err => this.error = err.message
        });
      }

      updateVisibilityDonation(publicId:string){

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        this.donationService.updateVisibilityDoanation(publicId).subscribe({
          next: ()=>{

              this.captchaToken=null;

              this.hideModal('visibilityModal');

              // Mise à jour du tableau principal
              this.fetchDonations();

              // Rchargement les dons
              this.loadDonations();
            },
          error: err => this.error = err.message
        });
      }

      updateClosureStatusDonation(publicId: string){

        if (!this.authService.isSupAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        if(!this.captchaToken){
            return;
        }

        const data = {

            captchaToken:this.captchaToken

        };

        this.donationService.updateClosureStatusDoantion(publicId, data).subscribe({
          next: ()=>{

              this.captchaToken=null;

              this.hideModal('closureStatusModal');

              // Mise à jour du tableau principal
              this.fetchDonations();

              // Rchargement les dons
              this.loadDonations();
            },
          error: err => this.error = err.message
        });
      }

      loadEventsByYear(year: number): void {

        this.donationService.getDonationsByYear(year)
          .subscribe({
            next: (data) => {
              this.donations = data;
            },
            error: (error) => {
              console.error('Erreur lors du chargement des événements', error);
            }
          });
      }

      loadEventsByMont(year: number, month: number): void {

        this.donationService.getDonationsByMonth(year, month)
          .subscribe({
            next: (data) => {
              this.donations = data;
            },
            error: (error) => {
              console.error('Erreur lors du chargement des événements', error);
            }
          });
      }


      fetchDonations(){
        if ($.fn.DataTable.isDataTable('#example1')) {
          $('#example1').DataTable().destroy();
        }

        this.donationService.getCountDonationsByBeneficiary().subscribe({
          next: (data) => {
            this.beneficiariesCount = data;

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

      openDonationsModal(beneficiaryId: number, evenTypeName: string){

        this.currentBeneficiaryId = beneficiaryId;
        this.currentEvenTypeName = evenTypeName;

        this.loadDonations();
      }

      loadDonations(){

        this.beneficiaryName = this.currentEvenTypeName;

        if ($.fn.DataTable.isDataTable('#donationsTable')) {
          $('#donationsTable').DataTable().destroy();
        }

        this.donationService.findDonationsBybenecifiaryId(this.currentBeneficiaryId).subscribe({
          next: (data) => {
            this.donations = data;
            this.showModal('donationsModal');

            setTimeout(() => {

              $('#eventsTable').DataTable({
                language: DATATABLE_FR,
                destroy: true
              });

            }, 300);
          },
          error: (err) => console.log(err)
        });
      }

      getDonationParticipations(donation: Donation){
        this.titleDonation = donation.title;
        this.participantService.getParticipantsByDonation(donation.publicId!).subscribe({
          next: (data) => {
            this.participants = data;
            this.showModal('participantsModal');
          },
          error: (err) => console.log(err)
        });

      }

      getBeneficiaries(){
        this.beneficiaryService.getBeneficiaries().subscribe({
          next: (data) => this.beneficiaries = data,
          error: (err) => console.log(err)
        });
      }

      onFileSelected(event: any) {
        if (event.target.files.length > 0) {
          this.selectedFile = event.target.files[0];

          const reader = new FileReader();
          reader.onload = () => {
            this.photoPreview = reader.result as string;
          };
          reader.readAsDataURL(this.selectedFile);
        }
      }

      openAddModal(){
        this.errorMessage = '';
        this.initForm();
        this.showModal('addDonationModal');
      }

      addDonation(){

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        const formData = new FormData();

        formData.append(
          'data',
          new Blob([JSON.stringify(this.donationForm.value)], { type: 'application/json' })
        );

        if (this.selectedFile) {
          formData.append('photo', this.selectedFile);
        }

        this.donationService.addDonation(formData).subscribe({
          next: () => {
            this.initForm();
            this.statusInfo = true;
            this.fetchDonations();
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
      this.donationService.getDonation(publicId).subscribe({
        next: (data) => {
          this.publicId = data.publicId;
          this.photoPreview = data.photo!;

          this.donationForm = this.fb.group({
            title: data.title,
            description: data.description,
            dateDonation: data.dateDonation,
            beneficiaryId: data.beneficiaryId
          });

          this.showModal('updateDonationModal');
        },
        error: (err) => console.log(err)
      })
    }

    updDonation() {

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }

      const formData = new FormData();

      formData.append(
        'data',
        new Blob([JSON.stringify(this.donationForm.value)], { type: 'application/json' })
      );

      if (this.selectedFile) {
        formData.append('photo', this.selectedFile);
      }

      this.donationService.updateDonation(this.publicId, formData).subscribe({
        next: () => {
          this.statusInfo = false;
          this.fetchDonations();
          this.loadDonations();
          this.showModal('infoModal');
        },
        error: (err) => {
          console.log(err);
          this.errorMessage = err.error;
        }
      });
    }
}
