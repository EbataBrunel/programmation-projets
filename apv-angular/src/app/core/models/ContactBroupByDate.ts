import { Contact } from "./Contact";

export interface ContactGroupByDate{
  date: Date;
  contacts: Contact[];
}
