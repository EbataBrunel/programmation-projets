export enum MessageStatus{
    SENT='SENT',
    DELIVERED='DELIVERED',
    READ='READ'
}

export interface Message{

  publicId: string;

  senderId: number;

  senderName?: string;

  receiverId: number;

  receiverName?: string;

  content: string;

  sentAt: string;

  status: MessageStatus;
}
