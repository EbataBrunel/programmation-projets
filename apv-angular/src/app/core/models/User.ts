import { Role } from "./Role";
import { UserProfile } from "./UserProfile";

export interface User{
  id?: number;
  publicId?: string;
  username: string;
  email: string;
  enabled: boolean;
  userProfile: UserProfile;
  roles?: Role[];
}
