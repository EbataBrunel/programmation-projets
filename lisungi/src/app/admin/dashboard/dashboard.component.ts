import { Component } from '@angular/core';
import { UserService } from 'src/app/core/services/user/user.service';
import { EventTypeService } from 'src/app/core/services/event-type/event-type.service';
import { EventType } from 'src/app/core/models/EventType';
import { EventService } from 'src/app/core/services/event/event.service';
import { ContributionService } from 'src/app/core/services/contribution/contribution.service';
import { RegulationService } from 'src/app/core/services/regulation/regulation.service';
import { NewsService } from 'src/app/core/services/news/news.service';
import { BeneficiaryService } from 'src/app/core/services/beneficiary/beneficiary.service';
import { DonationService } from 'src/app/core/services/donation/donation.service';
import { ParticipantService } from 'src/app/core/services/participant/participant.service';
import { ContactService } from 'src/app/core/services/contact/contact.service';
import { MessageService } from 'src/app/core/services/message/message.service';
import { ViewService } from 'src/app/core/services/view/view.service';
import { News } from 'src/app/core/models/News';
import { User } from 'src/app/core/models/User';
import { Event } from 'src/app/core/models/Event';
import { Contribution } from 'src/app/core/models/Contribution';
import { Regulation } from 'src/app/core/models/Regulation';
import { Beneficiary } from 'src/app/core/models/Beneficiary';
import { Donation } from 'src/app/core/models/Donation';
import { DonationParticipant } from 'src/app/core/models/DonationParticipant';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { Title } from '@angular/platform-browser';
import { SettingService } from 'src/app/core/services/setting/setting.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {

  typeEvents: EventType[] = [];
  events: Event[] = [];
  contributions: Contribution[] = [];
  regulations: Regulation[] = [];
  news: News[] = [];
  users: User[] = [];
  beneficiaries: Beneficiary[] = [];
  donations: Donation[] = [];
  participants: DonationParticipant[] = [];

  currentUserId = 0;
  countMessageUnread = 0;
  totalContactStatus = 0;
  countViews = 0;

  error: string = '';

  isAdmin$ = this.authService.isAdmin$;

  public constructor(
    private titleService: Title,
    private settingService: SettingService,
    private userService: UserService,
    private eventTypeService: EventTypeService,
    private eventService: EventService,
    private contributionService: ContributionService,
    private regulationService: RegulationService,
    private newsService: NewsService,
    private beneficiaryService: BeneficiaryService,
    private donationService: DonationService,
    private participantService: ParticipantService,
    private contactService: ContactService,
    private messageService: MessageService,
    private viewService: ViewService,
    private authService: AuthService
  ){
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Tableau de bord | ${setting.nameApp}`);
      }
    });
  }

  ngOnInit(){

      this.fetchEventTypes();
      this.fetchUsers();
      this.fetchEvents();
      this.fetchContributions();
      this.fetchNews();
      this.fetchRegulations();
      this.fetchBeneficiaries();
      this.fetchDonations();
      this.fetchParticipants();
      this.getTotalContactStatus();
      this.getCountMessageUnread();
      this.getCountViews();
  }

  fetchEventTypes(): void {
      this.eventTypeService.getEventTypes().subscribe({
        next: (data) => {
          this.typeEvents = data;
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

  fetchEvents(): void {
      this.eventService.getEvents().subscribe({
        next: (data) => {
          this.events = data;
        },
        error: err => this.error = err.message
      });
  }

  fetchContributions(): void {
      this.contributionService.getContributions().subscribe({
        next: (data) => {
          this.contributions = data;
        },
        error: err => this.error = err.message
      });
  }

  fetchRegulations(): void {
      this.regulationService.getRegulations().subscribe({
        next: (data) => {
          this.regulations = data;
        },
        error: err => this.error = err.message
      });
  }

  fetchNews(): void {
      this.newsService.getAllNews().subscribe({
        next: (data) => {
          this.news = data;
        },
        error: err => this.error = err.message
      });
  }

  fetchBeneficiaries(): void {
      this.beneficiaryService.getBeneficiaries().subscribe({
        next: (data) => {
          this.beneficiaries = data;
        },
        error: err => this.error = err.message
      });
  }

  fetchDonations(): void {
      this.donationService.getDonations().subscribe({
        next: (data) => {
          this.donations = data;
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

  getTotalContactStatus(){
    this.contactService.getCountContactStatus(0).subscribe({
      next: (data) => {
        this.totalContactStatus = data;
      },
      error: err => this.error = err.message
    });
  }

  getCountMessageUnread(){
    this.messageService.countUnread().subscribe({
      next: (count)  => {
        this.countMessageUnread = count;
      },
      error: err => this.error = err.message
    })
  }

  getCountViews(){
    this.viewService.getCountUsersNotViewWithAdmin().subscribe({
      next: (count)  => {
        this.countViews = count;
      },
      error: err => this.error = err.message
    })
  }
}
