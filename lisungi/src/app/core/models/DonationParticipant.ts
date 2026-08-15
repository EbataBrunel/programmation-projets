export interface DonationParticipant {
  id?: number;

  publicId?: string;

  name: string;

  itemType: string;

  description?: string;

  amount?: number; // uniquement si itemType == MONEY

  participationDate?: Date;

  donationId: number|null;

  donationTitle?: string;

  userId?: number;

  userLastName?: string;

  userFirstName?: string;
}
