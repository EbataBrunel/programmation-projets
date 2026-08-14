import { Component } from '@angular/core';
import { DonationService } from 'src/app/core/services/donation/donation.service';
import { Donation } from 'src/app/core/models/Donation';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-customer-service',
  templateUrl: './customer-service.component.html',
  styleUrls: ['./customer-service.component.css']
})
export class CustomerServiceComponent {

  donations: Donation[] = [];
  error: string = '';
  selectedImage: string | null = null;

  constructor(
    private titleService: Title,
    private settingService: SettingService,
    private donationService: DonationService
  ) {
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Services | ${setting.nameApp}`);
      }
    });
  }

  ngOnInit(): void {
      this.fetchNews();
  }

  fetchNews(): void {

      this.donationService.getDonations().subscribe({
          next: (data) => {
            this.donations = data.filter( donation => donation.publicStatus == true);
          },
          error: err => this.error = err.message
      });
  }

  openImage(photo: string): void {
      this.selectedImage = 'http://127.0.0.1:8080/uploads/' + photo;
  }

  closeImage(): void {
      this.selectedImage = null;
  }

}
