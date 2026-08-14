import { Component } from '@angular/core';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { UserProfileService } from 'src/app/core/services/userProfile/user-profile.service';
import { ContactService } from 'src/app/core/services/contact/contact.service';
import { MessageService } from 'src/app/core/services/message/message.service';
import { ViewService } from 'src/app/core/services/view/view.service';
import { Conversation } from 'src/app/core/models/Conversation';

@Component({
  selector: 'app-admin-header',
  templateUrl: './admin-header.component.html',
  styles: [
  ]
})
export class AdminHeaderComponent {

    conversations: Conversation[] = [];

    user: any
    profile: any;

    countProfiles = 0;
    totalContactStatus = 0;
    countMessageUnread = 0;
    countNewsRegistrations = 0;
    countViews = 0;

    error: string = '';

    setting$ = this.settingService.setting$;
    isAdmin$ = this.authService.isAdmin$;
    isSupAdmin$ = this.authService.isSupAdmin$;

    constructor(
      private auth: AuthService,
      private settingService: SettingService,
      private profileService: UserProfileService,
      private contactService: ContactService,
      private messageService: MessageService,
      private viewService: ViewService,
      private authService: AuthService

    ){}

    ngOnInit() {

      // 1. Charger l'utilisateur connecté
      this.auth.getCurrentUser().subscribe({
        next: (data) => {
          this.user = data;
          this.profileService.getProfileByUser(data.publicId).subscribe(
            (profile) => {
              this.profileService.setProfile(profile);
            }
          );
        },
        error: (err) => console.error(err)
      });

      this.profileService.profile$.subscribe({
        next: (profile) => {

          if (profile) {
            this.profile = profile;
          }

        },
        error: (err) => console.error(err)
      });

      this.getTotalContactStatus();
      this.getCountMessageUnread();
      this.loadConversations();
      this.getCountTodayRegistrations();
      this.getCountViews();
      this.loadProfiles();
    }

    getTotalContactStatus(){
      this.contactService.getCountContactStatus(0).subscribe({
        next: (data) => {
          this.totalContactStatus = data;
        },
        error: (err) => console.log(err)
      });
    }

    loadConversations(){

      this.messageService.getConversations().subscribe({
        next:data => {
          this.conversations = data.filter(conversation => conversation.unreadCount > 0);
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

    getCountTodayRegistrations(){
      this.profileService.getTodayRegistrations().subscribe({
        next: (data) => {
          this.countNewsRegistrations = data.length;
        },
        error: (err) => console.log(err)
      });
    }

    getCountViews(){
      this.viewService.getCountUsersNotViewWithAdmin().subscribe({
        next: (count)  => {
          this.countViews = count;
        },
        error: err => this.error = err.message
      })
    }

    loadProfiles(){
      this.profileService.getProfilesByReasonRemovalNot().subscribe({
        next: (data) => {
          this.countProfiles = data.length;
        },
        error: (error) => {
          console.error('Erreur lors de la récupération des profils', error);
        }
      });
    }
}
