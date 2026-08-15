export interface Contribution {

  publicId?: string;

  contributedId: number|null;

  eventId: number|null;

  eventName?: string;

  userId?: number;

  userLastName?: string;

  userFirstName?: string;

  amount: number;

  status?: Boolean;

  createdAt?: Date;
}
