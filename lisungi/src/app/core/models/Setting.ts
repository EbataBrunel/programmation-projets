export interface Setting{
  publicId?: number;
  nameApp: string;
  nameDev: string;
  version: string;
  theme: string|null;
  bodyTheme: string|null;
  textColor: string|null;
  currency: string;
  address: string;
  email: string;
  phone: string;
  logo: string;
  width: number;
  height: number;
}
