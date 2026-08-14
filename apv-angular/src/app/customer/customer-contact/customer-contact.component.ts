import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { ContactService } from 'src/app/core/services/contact/contact.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { Contact } from 'src/app/core/models/Contact';
import { Setting } from 'src/app/core/models/Setting';
import { Title } from '@angular/platform-browser';

declare var $: any;

@Component({
  selector: 'app-customer-contact',
  templateUrl: './customer-contact.component.html',
  styles: [
  ]
})
export class CustomerContactComponent {

    error: string = '';

    setting$ = this.settingService.setting$;

    contact: Contact = {
      'lastName': '',
      'firstName': '',
      'email': '',
      'phone': '',
      'status': 0,
      'message': ''
    }

    constructor(
      private titleService: Title,
      private settingService: SettingService,
      private contactservice: ContactService){
        this.settingService.setting$.subscribe(setting => {
          if (setting?.nameApp) {
            this.titleService.setTitle(`Contact | ${setting.nameApp}`);
          }
        });
      }

    addContact(form: NgForm){

      if (form.invalid) return;

      this.contactservice.addContact(this.contact).subscribe(
        data => {
            form.resetForm({
              'lastName': '',
              'firstNme': '',
              'email': '',
              'phone': '',
              'message': ''
            });

            $('#info-modal').modal('show');
        }
      )
    }
}
