import { Contribution } from "./Contribution";

export interface Event {

  id?: number;

  publicId?: string;

  name: string;

  mount: number | null;

  amountTotal?: number | null;

  eventDate: Date | null;

  closure_status?: Boolean;

  comment: string;

  eventTypeId: number;

  eventTypeName?: string;

  userId: number;

  userLastName?: string;

  userFirstName?: string;

  contributions?: Contribution[];
}
