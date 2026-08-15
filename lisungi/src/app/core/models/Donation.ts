import { DonationParticipant } from "./DonationParticipant";

export interface Donation {
  id?: number;

  publicId?: string;

  title: string;

  description: string;

  dateDonation: Date;

  closure_status?: boolean;

  beneficiaryId: number|null;

  beneficiaryName?: string;

  photo: string|null;

  publicStatus?: boolean;

  participants?: DonationParticipant[];
}
