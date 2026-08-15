import { Component } from '@angular/core';
import { DonationService } from 'src/app/core/services/donation/donation.service';
import { ParticipantService } from 'src/app/core/services/participant/participant.service';
import { UserService } from 'src/app/core/services/user/user.service';
import { Donation } from 'src/app/core/models/Donation';
import { DonationParticipant } from 'src/app/core/models/DonationParticipant';
import { User } from 'src/app/core/models/User';
import { Title } from '@angular/platform-browser';
import { SettingService } from 'src/app/core/services/setting/setting.service';

@Component({
  selector: 'app-apropos',
  templateUrl: './apropos.component.html',
  styleUrls: ['./apropos.component.css']
})
export class AproposComponent {

    donations: Donation[] = [];
    participants: DonationParticipant[] = [];
    users: User[] = [];

    error: string = '';

    public constructor(
      private titleService: Title,
      private settingService: SettingService,
      private userService: UserService,
      private participantService: ParticipantService,
      private donationService: DonationService
    ){
      this.settingService.setting$.subscribe(setting => {
        if (setting?.nameApp) {
          this.titleService.setTitle(`A propos | ${setting.nameApp}`);
        }
      });
    }

    ngOnInit(): void {
        this.fetchDonations();
        this.fetchUsers();
        this.fetchParticipants();
    }

    fetchDonations(): void {
        this.donationService.getDonations().subscribe({
          next: (data) => {
            this.donations = data;
          },
          error: err => this.error = err.message
        });
    }

    fetchUsers(): void {
        this.userService.getUsers().subscribe({
          next: (data) => {
            this.users = data;
          },
          error: err => this.error = err.message
        });
    }

    fetchParticipants(): void {
        this.participantService.getDonationParticipants().subscribe({
          next: (data) => {
            this.participants = data;
          },
          error: err => this.error = err.message
        });
    }
}
