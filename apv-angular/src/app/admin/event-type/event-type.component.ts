import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { EventTypeService } from 'src/app/core/services/event-type/event-type.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { EventType } from 'src/app/core/models/EventType';
import { DATATABLE_FR } from 'src/app/core/config/datatable-fr';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { Title } from '@angular/platform-browser';

declare var $: any;

@Component({
  selector: 'app-event-type',
  templateUrl: './event-type.component.html',
  styles: [
  ]
})
export class EventTypeComponent {
    event_types: EventType[] = [];
    selectedEventType!: EventType;

    error: string = '';
    errorMessage = '';

    publicId: any;

    statusInfo = true;

    eventTypeForm!: FormGroup;

    setting$ = this.settingService.setting$;
    isAdmin$ = this.authService.isAdmin$;

    constructor(
      private fb: FormBuilder,
      private titleService: Title,
      private eventTypeService: EventTypeService,
      private settingService: SettingService,
      private authService: AuthService
    ) {
      this.settingService.setting$.subscribe(setting => {
        if (setting?.nameApp) {
          this.titleService.setTitle(`Types d'évènements | ${setting.nameApp}`);
        }
      });
    }

    ngOnInit(): void {
      this.initForm();
      this.fetchEventTypes();
    }

    private showModal(id: string) {
      $('#' + id).modal('show');
    }

    private hideModal(id: string) {
      $('#' + id).modal('hide');
    }

    initForm() {
      this.eventTypeForm = this.fb.group({
        name: ['', Validators.required]
      });
    }

    openDeleteModal(eventType: any) {
        this.selectedEventType = eventType;

        this.showModal('deleteModal');
    }

    deleteEventType(publicId: string){

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }

      this.eventTypeService.deleteEventType(publicId).subscribe({
        next: () =>{
          this.fetchEventTypes();
          this.hideModal('deleteModal');
        },
        error: err => this.error = err.message
      });
    }

    fetchEventTypes(): void {

      if ($.fn.DataTable.isDataTable('#example1')) {
        $('#example1').DataTable().destroy();
      }

      this.eventTypeService.getEventTypes().subscribe({
        next: (data) => {
          this.event_types = data;

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
      this.showModal('addEventTypeModal');
    }

    addEventType(){

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }

      const formData = new FormData();

      formData.append(
        'data',
        new Blob([JSON.stringify(this.eventTypeForm.value)], { type: 'application/json' })
      );

      this.eventTypeService.addEventType(formData).subscribe({
        next: () => {
          this.initForm();
          this.statusInfo = true;
          this.fetchEventTypes();
          this.showModal('infoModal');
        },
        error: (err) => {

          console.log(err);

          this.errorMessage = err.error;
          ;

        }
      });
    }

    openUpdateModal(publicId: string){

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }

      this.errorMessage = '';

      this.eventTypeService.getEventType(publicId).subscribe({
        next: (data) => {
          this.publicId = data.publicId;

          this.eventTypeForm = this.fb.group({
            name: data.name
          });

          this.showModal('updateEventTypeModal');
        },
        error: err => this.error = err.message
      });
    }

    updEventType() {

      const formData = new FormData();

      formData.append(
        'data',
        new Blob([JSON.stringify(this.eventTypeForm.value)], { type: 'application/json' })
      );

      this.eventTypeService.updateEventType(this.publicId, formData).subscribe({
        next: () => {
          this.statusInfo = false;
          this.fetchEventTypes();
          this.showModal('infoModal');
        },
        error: (err) => {

          console.log(err);

          this.errorMessage = err.error;

        }
      });
    }
}
