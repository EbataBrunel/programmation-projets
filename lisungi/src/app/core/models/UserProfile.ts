export interface UserProfile{
  publicId?: string;
  firstName: string;
  lastName: string;
  gender?: string;
  phone: string;
  address: string;
  country: string;
  city: string;
  borough: string;
  profession?: string;
  photo: string;
  registrationDate?: Date;
  reasonRemoval?: string;
  userId: number;
  userName: string;
  userEmail: string;
}
