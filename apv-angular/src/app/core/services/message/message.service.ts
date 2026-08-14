import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MessageRequest } from '../../models/MessageRequest';
import { Message } from '../../models/Message';
import { Conversation } from '../../models/Conversation';
import { environment } from 'src/app/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MessageService {

  private apiUrl = `${environment.apiUrl}/messages`;

  constructor(
    private http:HttpClient
  ){}

  sendMessage(data:MessageRequest):Observable<Message>{
    return this.http.post<Message>(this.apiUrl, data );
  }

  getConversation(otherUserId:number ):Observable<Message[]>{
    return this.http.get<Message[]>(
      `${this.apiUrl}/conversation`,
      {params:{otherUserId}});
  }

  getConversations():Observable<Conversation[]>{

    return this.http.get<Conversation[]>(`${this.apiUrl}/conversations`);

  }

  markAsRead(otherUserId:number){
    return this.http.patch<void>(
      `${this.apiUrl}/read`,{},{ params:{otherUserId}});
  }

  countUnread():Observable<number>{
    return this.http.get<number>(`${this.apiUrl}/unread`);
  }

  deleteMessage(publicId: string) {

    return this.http.delete<void>(
      `${this.apiUrl}/${publicId}`
    );

  }
}
