export interface Contact {
    publicId?: string;
    lastName: string;
    firstName: string;
    email: string;
    phone: string;
    message: string;
    status: number;
    createdAt?: Date;
}
