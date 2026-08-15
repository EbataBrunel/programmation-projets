export interface Beneficiary {
  id?: number;

  publicId?: string;

  name: string;

  phone?: string;

  email?: string;

  address: string;

  country: string;

  city: string;

  borough: string;

  type: string;

  dateExistence: Date;
}
