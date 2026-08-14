import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { MessageService } from 'src/app/core/services/message/message.service';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { UserService } from 'src/app/core/services/user/user.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { Message } from 'src/app/core/models/Message';
import { Conversation } from 'src/app/core/models/Conversation';
import { User } from 'src/app/core/models/User';
import { MessageRequest } from 'src/app/core/models/MessageRequest';
import { Title } from '@angular/platform-browser';

declare var $: any;

@Component({
  selector: 'app-message',
  templateUrl: './message.component.html',
  styleUrls: ['./message.component.css']
})
export class MessageComponent implements OnInit{

  messages: Message[] = [];
  conversations: Conversation[] = [];
  users: User[] = [];

  currentUserId = 0;
  selectedUserId!: number|null;
  selectedUserName!: string;
  selectedUserPhoto!: string;
  userId!: number|null;
  error: string = '';
  newMessage = "";

  setting$ = this.settingService.setting$;

  message: MessageRequest = {
    senderId: 0,
    receiverId: 0,
    content: ''
  };


  constructor(
    private titleService: Title,
    private messageService: MessageService,
    private auth: AuthService,
    private userService: UserService,
    private settingService: SettingService
  ){
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Messages | ${setting.nameApp}`);
      }
    });
  }

  ngOnInit(){

    // Charger l'utilisateur connecté
    this.auth.getCurrentUser().subscribe({
      next: (data) => {
        this.currentUserId = data.id;
      },
      error: (err) => console.error(err)
    });

    this.loadConversations();
  }

  private showModal(id: string) {
    $('#' + id).modal('show');
  }

  private hideModal(id: string) {
    $('#' + id).modal('hide');
  }

  getUsers(){
    this.userService.getUsers().subscribe({
      next: (data) => {
        this.users = data.filter(user => user.id !== Number(this.currentUserId));
      },
      error: (err) => console.log(err)
    });
  }

  openUserModal(){
    this.selectedUserId = null;
    this.userId = null;
    this.getUsers();
    this.showModal('usersModal');
  }

  onUserChange(event: globalThis.Event) {

    const value = (event.target as HTMLSelectElement).value;

    // Réinitialiser le select des événements
    //this.contributionForm.get('eventId')?.reset();

    if (value !== null) {

      this.selectedUserId = Number(value);

    }else {
      this.selectedUserId = null;
    }
  }

  loadConversations(){

    this.messageService.getConversations().subscribe({
      next:data => {
        this.conversations = data;
      },
      error: err => this.error = err.message
    });

  }

  openConversation(conversation:Conversation){

    this.newMessage = '';

    this.selectedUserId = conversation.userId;
    this.selectedUserName = conversation.userName;
    this.selectedUserPhoto = conversation.userPhoto;

    this.messageService.getConversation(this.selectedUserId).subscribe({

      next: (data) => {
        this.messages = data;
        this.messageService.markAsRead(this.selectedUserId!).subscribe({
          next:() => {
            this.loadConversations();
            this.showModal("conversationModal");
          },
          error: err => this.error = err.message
        });

      },
      error: err => this.error = err.message

    });
  }

  send(){

    if(!this.newMessage.trim())
      return;

    this.messageService.sendMessage({
        senderId: this.currentUserId,
        receiverId: this.selectedUserId,
        content: this.newMessage
      }
    ).subscribe({

      next: (msg) => {
        this.messages.push(msg);
        this.newMessage = "";
        this.loadConversations();
        this.hideModal('usersModal');
      },
      error: err => this.error = err.message

    });

  }

  isMine(message:Message){

      return message.senderId === this.currentUserId;

  }

  deleteMessage(message: Message) {

    if (!confirm("Supprimer ce message ?")) {
      return;
    }

    const backup = [...this.messages];

    this.messages = this.messages.filter(
      m => m.publicId !== message.publicId
    );

    this.messageService.deleteMessage(message.publicId)
        .subscribe({

          error: () => {

            this.messages = backup;

            alert("La suppression a échoué.");

          }

    });

  }
}
