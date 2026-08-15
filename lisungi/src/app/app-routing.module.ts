import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CustomerLayoutComponent } from './layouts/customer-layout/customer-layout.component';
import { AdminLayoutComponent } from './layouts/admin-layout/admin-layout.component';
import { HomeComponent } from './customer/home/home.component';
import { LoginComponent } from './connexion/login/login.component';
import { AuthenticationLayoutComponent } from './layouts/authentication-layout/authentication-layout.component';
import { DashboardComponent } from './admin/dashboard/dashboard.component';
import { EventTypeComponent } from './admin/event-type/event-type.component';
import { LogoutComponent } from './connexion/logout/logout.component';
import { EventComponent } from './admin/event/event.component';
import { UserComponent } from './admin/user/user.component';
import { UserProfileComponent } from './admin/user-profile/user-profile.component';
import { ContributionComponent } from './admin/contribution/contribution.component';
import { MessageComponent } from './admin/message/message.component';
import { RegulationComponent } from './admin/regulation/regulation.component';
import { NewsComponent } from './admin/news/news.component';
import { SettingComponent } from './admin/setting/setting.component';
import { ForgotPasswordComponent } from './connexion/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './connexion/reset-password/reset-password.component';
import { RegisterComponent } from './connexion/register/register.component';
import { CustomerContactComponent } from './customer/customer-contact/customer-contact.component';
import { ContactComponent } from './admin/contact/contact.component';
import { BeneficiaryComponent } from './admin/beneficiary/beneficiary.component';
import { DonationComponent } from './admin/donation/donation.component';
import { DonationParticipantComponent } from './admin/donation-participant/donation-participant.component';
import { CustomerServiceComponent } from './customer/customer-service/customer-service.component';
import { AproposComponent } from './customer/apropos/apropos.component';
import { AuthGuardService } from './core/services/auth-guard/auth-guard.service';
import { StatistiqueComponent } from './admin/statistique/statistique.component';

const routes: Routes = [
  { path: "", pathMatch: "full", redirectTo: "home" },
  {
    path: '',
    component: CustomerLayoutComponent,
    children: [

      { path: 'home', component: HomeComponent },
      { path: 'customer-contact', component: CustomerContactComponent },
      { path: 'customer-service', component: CustomerServiceComponent },
      { path: 'a-propos', component: AproposComponent },
    ]
  },

  {
    path: '',
    component: AdminLayoutComponent,
    children: [

      { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuardService] },
      { path: 'event-types', component: EventTypeComponent, canActivate: [AuthGuardService] },
      { path: 'events', component: EventComponent, canActivate: [AuthGuardService] },
      { path: 'users', component: UserComponent, canActivate: [AuthGuardService] },
      { path: 'user-profile', component: UserProfileComponent, canActivate: [AuthGuardService] },
      { path: 'contributions', component: ContributionComponent, canActivate: [AuthGuardService] },
      { path: 'messages', component: MessageComponent, canActivate: [AuthGuardService] },
      { path: 'regulations', component: RegulationComponent, canActivate: [AuthGuardService] },
      { path: 'news', component: NewsComponent, canActivate: [AuthGuardService] },
      { path: 'contacts', component: ContactComponent, canActivate: [AuthGuardService] },
      { path: 'settings', component: SettingComponent, canActivate: [AuthGuardService] },
      { path: 'beneficiaries', component: BeneficiaryComponent, canActivate: [AuthGuardService] },
      { path: 'donations', component: DonationComponent, canActivate: [AuthGuardService] },
      { path: 'donation-participants', component: DonationParticipantComponent, canActivate: [AuthGuardService] },
      { path: 'statistique', component: StatistiqueComponent, canActivate: [AuthGuardService] },
    ]
  },

  {
    path: '',
    component: AuthenticationLayoutComponent,
    children: [
      { path: "register", component: RegisterComponent },
      { path: "login", component: LoginComponent },
      { path: "logout", component: LogoutComponent },
      { path: 'forgot-password', component: ForgotPasswordComponent },
      { path: 'reset-password', component: ResetPasswordComponent }
    ]
  },

  { path: '**', redirectTo: 'home' }, // si URL inconnue, on renvoie login
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
