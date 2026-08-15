import { Component } from '@angular/core';
import { switchMap } from 'rxjs';
import { formatDate } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { ContactService } from 'src/app/core/services/contact/contact.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { Contact } from 'src/app/core/models/Contact';
import { ContactGroupByDate } from 'src/app/core/models/ContactBroupByDate';
import { UpdateContactStatusRequest } from 'src/app/core/models/UpdateContactStatusRequest';
declare var $: any;

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styles: [
  ]
})
export class ContactComponent {
  contacts: Contact[] = [];
  groupedContacts: ContactGroupByDate[] = [];
  updateContact : UpdateContactStatusRequest = {
    'status': 2
  }

  totalContactStatus: number = 0;
  selectedContact: any = null;

  contactLastname = '';
  contactFirstname = '';
  contactPhone = '';
  contactMessage = '';
  contactEmail = '';

  setting$ = this.settingService.setting$;

  constructor(
    private titleService: Title,
    private contactService: ContactService,
    private settingService: SettingService
  ){
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Contacts | ${setting.nameApp}`);
      }
    });
  }

  ngOnInit() {
    this.loadContacts();
  }

  loadContacts() {
    this.contactService.updateAllStatus().pipe(
      switchMap((res) => {
          return this.contactService.getContacts();
      })
    ).subscribe(data => {
      this.groupedContacts = data;
      this.getTotalContactStatus();
    });
  }

  public isToday(date: Date): boolean {
    const todayString = this.getToday();

    const dateObj = new Date(date);
    const dateString =
      dateObj.getFullYear() + '-' +
      String(dateObj.getMonth() + 1).padStart(2, '0') + '-' +
      String(dateObj.getDate()).padStart(2, '0');

    return dateString === todayString;
  }

  public getToday(): string {
    const today = new Date();

    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
  }

  //
  public getToday2(): string {
    return formatDate(new Date(), 'yyyy-MM-dd', 'en');
  }

  public isToday2(date: Date): boolean {
    const today = formatDate(new Date(), 'yyyy-MM-dd', 'en');
    const itemDate = formatDate(date, 'yyyy-MM-dd', 'en');
    return today === itemDate;
  }

  openDetail(publicId: string){
    this.contactService.getContact(publicId).pipe(
      switchMap((data) => {

        this.contactLastname = data.lastName;
        this.contactFirstname = data.firstName;
        this.contactPhone = data.phone;
        this.contactMessage = data.message;
        this.contactEmail = data.email;

        return this.contactService.updateStatus(data.publicId!, this.updateContact)
      })
    ).subscribe({
      next: (res) => {
        this.loadContacts();
        this.getTotalContactStatus();
        $('#detailModal').modal('show');
      },
      error: (err) => console.log(err)
    });

  }

  getTotalContactStatus(){
    this.contactService.getCountContactStatus(1).subscribe(data => {
      this.totalContactStatus = data;
    });
  }

  openDeleteModal(contact: any) {
    this.selectedContact = contact;

    // Initialisation de la modal Bootstrap
    const modalElement = document.getElementById('deleteModal');
    if (modalElement) {
      $('#deleteModal').modal('show');
    }
  }

  deleteContact(publicId:string){
    this.contactService.deleteContact(publicId).subscribe(
          data=>{
            $('#deleteModal').modal('hide');
             this.loadContacts();
          }
    );
  }
}
