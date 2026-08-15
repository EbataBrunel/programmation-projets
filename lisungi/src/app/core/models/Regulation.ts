export interface Regulation {

  publicId?: string;

  name: string | null;

  description: string;

  createdAt?: Date;

  updateAt?: Date;

  userId?: number;

  userLastName?: string;

  userFirstName?: string;
}
