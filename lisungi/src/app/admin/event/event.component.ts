import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Title } from '@angular/platform-browser';
import { EventService } from 'src/app/core/services/event/event.service';
import { ContributionService } from 'src/app/core/services/contribution/contribution.service';
import { EventTypeService } from 'src/app/core/services/event-type/event-type.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { UserService } from 'src/app/core/services/user/user.service';
import { Contribution } from 'src/app/core/models/Contribution';
import { Event } from 'src/app/core/models/Event';
import { EventType } from 'src/app/core/models/EventType';
import { User } from 'src/app/core/models/User';
import { EventTypeCount } from 'src/app/core/models/EventTypeCount';
import { DATATABLE_FR } from 'src/app/core/config/datatable-fr';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { EventCountByYear } from 'src/app/core/models/EventCountByYear';

declare var $: any;

@Component({
  selector: 'app-event',
  templateUrl: './event.component.html',
  styles: [
  ]
})
export class EventComponent {
      events: Event[] = [];
      eventsStat: Event[] = [];
      contributions: Contribution[] = [];
      eventTypes: EventType[] = [];
      eventTypesCount: EventTypeCount[] = [];
      users: User[] = [];
      eventsByYear: EventCountByYear[] = [];
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
      selectedEvent: Event | null = null;

      error: string = '';
      errorMessage = '';
      year!: number|null;
      month!: number|null;

      captchaToken: string | null = null;

      eventTypeName!: string;
      nameEvent!: string;

      currentEventTypeId!: number;
      currentEventTypeName!: string;

      event: Event = {
        name: '',
        mount: 0,
        eventDate: null,
        closure_status: false,
        comment: '',
        eventTypeId: 0,
        userId: 0
      };

      statusInfo = true;

      setting$ = this.settingService.setting$;
      isAdmin$ = this.authService.isAdmin$;
      isSupAdmin$ = this.authService.isSupAdmin$

      constructor(
        private titleService: Title,
        private contributionService: ContributionService,
        private eventService: EventService,
        private eventTypeService: EventTypeService,
        private userService: UserService,
        private settingService: SettingService,
        private authService: AuthService
      ) {
        this.settingService.setting$.subscribe(setting => {
          if (setting?.nameApp) {
            this.titleService.setTitle(`Evènements | ${setting.nameApp}`);
          }
        });
      }

      ngOnInit(): void {
        this.fetchEvents();
        this.getTypeEvents();
        this.getUsers();
        this.loadEventsByYearCount();
        this.resetEventForm();
      }

      private resetEventForm() {
        this.event = {
          name: '',
          mount: null,
          eventDate: null,
          closure_status: false,
          comment: '',
          eventTypeId: 0,
          userId: 0
        };
      }

      private showModal(id: string) {
          $('#' + id).modal('show');
      }

      private hideModal(id: string) {
          $('#' + id).modal('hide');
      }

      openDeleteModal(event: Event) {
        this.selectedEvent = event;

        this.showModal('deleteModal');

      }

      openDetailModal(event: Event){
        this.selectedEvent = event;
        this.showModal('detailModal');
      }

      openStatEvent(){
        this.year = null;
        this.showModal('statModal');
      }

      onYearChange(event: globalThis.Event) {

          this.month = null;

          const value = (event.target as HTMLSelectElement).value;

          if (value !== null) {

            this.year = Number(value);

            this.loadEventsByYear(this.year)

          } else {
            this.year = 0;
          }
      }

      onMonthChange(event: globalThis.Event) {

          const value = (event.target as HTMLSelectElement).value;

          if (value !== null) {

            this.month = Number(value);

            this.loadEventsByMonth(this.year!, this.month)

          } else {
            this.year = 0;
          }
      }

      openClosureStatusModal(event: Event){
        this.selectedEvent = event;
        this.showModal('closureStatusModal');
      }

      captchaResolved(token: string | null) {

        this.captchaToken = token;

      }

      loadEventsByYear(year: number): void {

        this.eventService.getEventsByYear(year)
          .subscribe({
            next: (data) => {
              this.eventsStat = data;
            },
            error: (error) => {
              console.error('Erreur lors du chargement des événements', error);
            }
          });
      }

      loadEventsByMonth(year: number, month: number): void {

        this.eventService.getEventsByMonth(year, month)
          .subscribe({
            next: (data) => {
              this.eventsStat = data;
            },
            error: (error) => {
              console.error('Erreur lors du chargement des événements', error);
            }
          });
      }

      loadEventsByYearCount(): void {
        this.eventService.countEventsByYear().subscribe({
          next: (data) => {
            this.eventsByYear = data;
          },
          error: (error) => {
            console.error(
              'Erreur lors du chargement des statistiques',
              error
            );
          }
        });
      }

      deleteEvent(publicId: string){

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        this.eventService.deleteEvent(publicId).subscribe({
          next: ()=>{
              this.hideModal('deleteModal')

              // Mise à jour du tableau principal
              this.fetchEvents();

              // Rchargement les évènements
              this.loadEvents();
          },
          error: err => this.error = err.message
        });
      }

      updateClosureStatusEvent(publicId: string){

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

        this.eventService.updateClosureStatusEvent(publicId, data).subscribe({
          next: ()=>{

              this.captchaToken=null;

              this.hideModal('closureStatusModal');

              // Mise à jour du tableau principal
              this.fetchEvents();

              // Rchargement les évènements
              this.loadEvents();
            },
          error: err => this.error = err.message
        });
      }

      fetchEvents(): void {
        if ($.fn.DataTable.isDataTable('#example1')) {
          $('#example1').DataTable().destroy();
        }

        this.eventService.getCountEventsByEventType().subscribe({
          next: (data) => {
            this.eventTypesCount = data;

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

      openEventsModal(evenTypeId: number, evenTypeName: string){

        this.currentEventTypeId = evenTypeId;
        this.currentEventTypeName = evenTypeName;

        this.loadEvents();

      }

      loadEvents(){

        this.eventTypeName = this.currentEventTypeName;

        if ($.fn.DataTable.isDataTable('#eventsTable')) {
          $('#eventsTable').DataTable().destroy();
        }

        this.eventService.findEventsByEventTypeId(this.currentEventTypeId).subscribe({
          next: (data) => {
            this.events = data;
            this.showModal('eventsModal');

            setTimeout(() => {

              $('#eventsTable').DataTable({
                destroy: true
              });

            }, 300);
          },
          error: (err) => console.log(err)
        });
      }

      getContributions(event: Event){
        this.nameEvent = event.name;
        this.contributionService.getContributionByEvent(event.publicId!).subscribe({
          next: (data) => {
            this.contributions = data;
            this.showModal('contributionsModal');
          },
          error: (err) => console.log(err)
        });

      }

      getTypeEvents(){
        this.eventTypeService.getEventTypes().subscribe({
          next: (data) => this.eventTypes = data,
          error: (err) => console.log(err)
        });
      }

      getUsers(){
        this.userService.getUsers().subscribe({
          next: (data) => this.users = data,
          error: (err) => console.log(err)
        });
      }

      openAddModal(){
        this.resetEventForm();
        this.errorMessage = '';
        this.showModal('addEventModal');
      }

      addEvent(form: NgForm){

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        this.eventService.addEvent(this.event).subscribe({
          next: () => {
            // Réinitialisation complète du formulaire
            form.resetForm();

            this.resetEventForm();

            this.statusInfo = true;
            this.fetchEvents();
            this.showModal('infoModal');
          },
          error: (err) => {

            console.log(err);

            this.errorMessage = err.error;

          }
        });
      }

      openUpdateModal(publicId: any){
        this.eventService.getEvent(publicId).subscribe({
          next:data => {
            this.errorMessage = '';
            this.event = { ...data };
            this.showModal('updateEventModal');
          }
        });
      }

      updEvent(form: NgForm) {

        if (!this.authService.isAdmin()) {
          this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
          return;
        }

        if (form.invalid) {
          return;
        }

        this.eventService.updateEvent(this.event).subscribe({
          next: () => {
            this.statusInfo = false;
            this.fetchEvents();
            this.loadEvents();
            this.showModal('infoModal');
          },
          error: (err) => {

            console.log(err);

            this.errorMessage = err.error;

          }
        });
      }
}
