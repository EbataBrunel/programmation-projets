export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  confirmPassword?: string; // seulement côté frontend
}
