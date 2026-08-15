import { Role } from "./Role";
export interface AuthResponse {
  id: number;
  publicId: string;
  userName: string;
  email: string;
  Roles: Role[];
}
