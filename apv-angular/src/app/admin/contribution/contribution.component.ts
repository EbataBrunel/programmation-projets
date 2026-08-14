import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { switchMap } from 'rxjs';
import { Title } from '@angular/platform-browser';
import { EventService } from 'src/app/core/services/event/event.service';
import { ContributionService } from 'src/app/core/services/contribution/contribution.service';
import { UserService } from 'src/app/core/services/user/user.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { EventType } from 'src/app/core/models/EventType';
import { EventTypeCount } from 'src/app/core/models/EventTypeCount';
import { Contribution } from 'src/app/core/models/Contribution';
import { User } from 'src/app/core/models/User';
import { ContributionsByEventCount } from 'src/app/core/models/ContributionsByEventCount';
import { EventTypeContributionCount } from 'src/app/core/models/EventTypeContributionCount';
import { Event } from 'src/app/core/models/Event';
import { DATATABLE_FR } from 'src/app/core/config/datatable-fr';
import { ContributedCount } from 'src/app/core/models/ContributedCount';

declare var $: any;


@Component({
  selector: 'app-contribution',
  templateUrl: './contribution.component.html',
  styles: [
  ]
})
export class ContributionComponent {
        eventTypeCount: EventTypeContributionCount[] = [];
        contributions: Contribution[] = [];
        countEventsByEventType: EventTypeCount[] = []
        events: Event[] = [];
        eventTypes: EventType[] = [];
        contributionsEvent: ContributionsByEventCount[] = [];
        users: User[] = []
        contributedCount: ContributedCount[] = [];
        contributionsByContributed: Contribution[] = [];
        selectedContribution!: Contribution;

        eventTypeId: number | null = null;
        eventTypeName!: string;
        eventName!: string;
        error: string = '';
        errorMessage = '';

        contributedPublicId!: string|null;
        contributedLastName!: string;
        contributedFirstName!: string;

        publicId: any;
        closure_status!: boolean;
        mount!: number;
        amountTotal!: number;

        currentEventPublicId!: string;
        currentEventName!: string;
        curentEventTypePublicId!: string;
        curentEventTypeName!: string;

        contributionForm!: FormGroup;
        statusInfo = true;
        submitted = false;

        setting$ = this.settingService.setting$;
        isAdmin$ = this.authService.isAdmin$;

        constructor(
          private fb: FormBuilder,
          private titleService: Title,
          private contributionService: ContributionService,
          private eventService: EventService,
          private userService: UserService,
          private settingService: SettingService,
          private authService: AuthService
        ) {
          this.settingService.setting$.subscribe(setting => {
            if (setting?.nameApp) {
              this.titleService.setTitle(`Contributions | ${setting.nameApp}`);
            }
          });
        }

        ngOnInit(): void {
          this.initForm();
          this.fetchEventTypes();
          this.getTypeEvents();
          this.getUsers();
        }

        initForm() {
          this.contributionForm = this.fb.group({
            amount: ['', Validators.required],
            contributedId: [null, Validators.required],
            eventId: [null, Validators.required],

          });
        }

        private showModal(id: string) {
          $('#' + id).modal('show');
        }

        private hideModal(id: string) {
            $('#' + id).modal('hide');
        }

        openContributedModal(){
          this.contributedPublicId = null;
          this.getCountContributionsByContributed();
          this.showModal('contributedModal');
        }

        onContributedChange(event: globalThis.Event) {

          const value = (event.target as HTMLSelectElement).value;

          if (value !== null) {

            this.contributedPublicId = value;

            this.getContributionsByContributed(this.contributedPublicId);

            this.getContributedByPublicId(this.contributedPublicId);

          } else {
            this.contributedPublicId = null;
          }
        }

        getCountContributionsByContributed(){
          this.contributionService.getCountContributionsByContributed().subscribe({
            next: (data) => this.contributedCount = data,
            error: (err) => console.log(err)
          });
        }

        getContributedByPublicId(contributedPublicId: string){
          this.userService.getUser(contributedPublicId).subscribe({
            next: (data) => {
              this.contributedLastName = data.userProfile.lastName;
              this.contributedFirstName = data.userProfile.firstName;
            },
            error: (err) => console.log(err)
          });
        }

        getContributionsByContributed(contributedPublicId: string){

          if ($.fn.DataTable.isDataTable('#contributedTable')) {
            $('#contributedTable').DataTable().destroy();
          }

          this.contributionService.getContributionsByContributed(contributedPublicId).subscribe({
            next: (data) => {
              this.contributionsByContributed = data;

              setTimeout(() => {
                $('#contributedTable').DataTable({
                  language: DATATABLE_FR,
                  destroy: true
                });
              }, 100);
            },
            error: (err) => console.log(err)
          });
        }

        getTypeEvents(){
          this.eventService.getCountEventsByEventType().subscribe({
            next: (data) => this.countEventsByEventType = data,
            error: (err) => console.log(err)
          });
        }

        getUsers(){
          this.userService.getUsers().subscribe({
            next: (data) => this.users = data,
            error: (err) => console.log(err)
          });
        }

        fetchEventTypes(): void {

          if ($.fn.DataTable.isDataTable('#example1')) {
            $('#example1').DataTable().destroy();
          }

          this.contributionService.getCountEventByEventTypeWithContribution().subscribe({
            next: (data) => {
              this.eventTypeCount = data;

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

        onEventTypeChange(event: globalThis.Event) {

          const value = (event.target as HTMLSelectElement).value;

          // Réinitialiser le select des événements
          this.contributionForm.get('eventId')?.reset();

          if (value !== null) {

            this.eventTypeId = Number(value);

            this.eventService.findEventsByEventTypeId(this.eventTypeId)
              .subscribe({
                next: (data) => {
                  this.events = data.filter(event => event.closure_status === false);
                },
                error: (err) => console.log(err)
            });

          } else {
            this.eventTypeId = null;
            this.events = [];
            this.submitted = false;
          }
        }

        openEventsModal(eventTypePublicId: string, eventTypeName: string){

          this.curentEventTypePublicId = eventTypePublicId;
          this.curentEventTypeName = eventTypeName;

          this.loadEvents();
        }

        loadEvents(){
          this.eventTypeName = this.curentEventTypeName;

          if ($.fn.DataTable.isDataTable('#eventsTable')) {
            $('#eventsTable').DataTable().destroy();
          }

          this.contributionService.getCountContributionsByEventAndEventType(this.curentEventTypePublicId).subscribe({
            next: (data) => {
              this.contributionsEvent = data;
              this.showModal('eventsModal');
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

        openContributionModal(eventPublicId: string, eventName: string, closure_status: boolean, mount: number, amountTotal: number){
          this.currentEventPublicId = eventPublicId;
          this.currentEventName = eventName;
          this.closure_status = closure_status;
          this.mount = mount;
          this.amountTotal = amountTotal;

          this.loadContributions();
        }

        loadContributions() {

          this.eventName = this.currentEventName;

          if ($.fn.DataTable.isDataTable('#contributionsTable')) {
            $('#contributionsTable').DataTable().destroy();
          }

          this.contributionService.getContributionByEvent(this.currentEventPublicId).subscribe({
                next: data => {

                  this.contributions = data;
                  this.showModal('contributionsModal');
                  setTimeout(() => {
                    $('#contributionsTable').DataTable({
                      language: DATATABLE_FR,
                      destroy: true
                    });
                  }, 300);

                },
                error: err => console.log(err)
              });
        }

        openDeleteModal(contribution: Contribution) {
          this.selectedContribution = contribution;
          this.showModal('deleteModal');
        }

        deleteContribution(publicId:any){

          if (!this.authService.isAdmin()) {
            this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
            return;
          }

            this.contributionService.deleteContribution(publicId).subscribe({
              next: () => {
                this.hideModal('deleteModal');

                // Mise à jour du tableau principal
                this.fetchEventTypes();

                // Recharger les évènements
                this.loadEvents();

                // Recharge uniquement les contributions
                this.loadContributions();
              },
            error: (err) => console.log(err)
          });
        }


        openAddModal(){
          this.errorMessage = '';
          this.initForm();
          this.showModal('addContributionModal');
        }

        addContribution(){

          if (!this.authService.isAdmin()) {
            this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
            return;
          }

          this.submitted = true;
          this.errorMessage = '';

          if (this.eventTypeId === null) {
            return;
          }

          const formData = new FormData();

          formData.append(
            'data',
            new Blob([JSON.stringify(this.contributionForm.value)], { type: 'application/json' })
          );

          this.contributionService.addContribution(formData).subscribe({
            next: () => {
              // Réinitialisation complète du formulaire
              this.initForm();
              this.statusInfo = true;
              this.fetchEventTypes();
              this.showModal('addContributionModal');
              this.showModal('infoModal');
            },
              error: (err) => {

              console.log(err);

              this.errorMessage = err.error;

            }
          });
        }

        openUpdateModal(publicId: string) {

          this.errorMessage = '';

          this.contributionService.getContribution(publicId)
            .pipe(
              switchMap(contribution => {

                this.publicId = contribution.publicId;

                this.contributionForm.patchValue({
                  amount: contribution.amount,
                  contributedId: contribution.contributedId,
                  eventId: contribution.eventId
                });

                return this.eventService.getEventById(contribution.eventId!);
              }),

              switchMap(event => {

                this.eventTypeId = event.eventTypeId;

                return this.eventService.findEventsByEventTypeId(event.eventTypeId);
              })
            )
            .subscribe({
              next: events => {
                this.events = events.filter(event => event.closure_status === false);
                this.showModal('updateContributionModal');
              },
              error: err => {
                console.log(err);
              }
            });
        }


        updContribution() {

          if (!this.authService.isAdmin()) {
            this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
            return;
          }

          this.errorMessage = '';
          this.submitted = true;

          const formData = new FormData();

          formData.append(
            'data',
            new Blob([JSON.stringify(this.contributionForm.value)], { type: 'application/json' })
          );

          this.contributionService.updateContribution(this.publicId, formData).subscribe({
            next:() => {
              this.statusInfo = false;
              this.fetchEventTypes();
              this.loadEvents();
              this.loadContributions();
              this.showModal('infoModal');
            },
              error: (err) => {

              console.log(err);

              this.errorMessage = err.error;

            }
          });
        }

        download() {

          this.contributionService.downloadPdf().subscribe(blob => {

            const url = window.URL.createObjectURL(blob);

            const a = document.createElement('a');

            a.href = url;

            a.download = 'contributions.pdf';

            a.click();

            window.URL.revokeObjectURL(url);

          });

        }
}
