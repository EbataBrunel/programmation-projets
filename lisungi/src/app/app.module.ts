import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { AuthInterceptor } from './core/interceptors/auth.interceptor';
import { RecaptchaModule } from 'ng-recaptcha';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './customer/home/home.component';
import { CustomerLayoutComponent } from './layouts/customer-layout/customer-layout.component';
import { CustomerHeaderComponent } from './layouts/customer-layout/customer-header/customer-header.component';
import { CustomerFooterComponent } from './layouts/customer-layout/customer-footer/customer-footer.component';
import { LoginComponent } from './connexion/login/login.component';
import { AuthenticationLayoutComponent } from './layouts/authentication-layout/authentication-layout.component';
import { AdminLayoutComponent } from './layouts/admin-layout/admin-layout.component';
import { DashboardComponent } from './admin/dashboard/dashboard.component';
import { AdminHeaderComponent } from './layouts/admin-layout/admin-header/admin-header.component';
import { AdminMenuComponent } from './layouts/admin-layout/admin-menu/admin-menu.component';
import { AdminFooterComponent } from './layouts/admin-layout/admin-footer/admin-footer.component';
import { EventTypeComponent } from './admin/event-type/event-type.component';
import { LogoutComponent } from './connexion/logout/logout.component';
import { EventComponent } from './admin/event/event.component';
import { ContributionComponent } from './admin/contribution/contribution.component';
import { UserComponent } from './admin/user/user.component';
import { UserProfileComponent } from './admin/user-profile/user-profile.component';
import { ContactComponent } from './admin/contact/contact.component';
import { MessageComponent } from './admin/message/message.component';
import { RegulationComponent } from './admin/regulation/regulation.component';
import { NewsComponent } from './admin/news/news.component';
import { SettingComponent } from './admin/setting/setting.component';
import { ForgotPasswordComponent } from './connexion/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './connexion/reset-password/reset-password.component';
import { RegisterComponent } from './connexion/register/register.component';
import { AproposComponent } from './customer/apropos/apropos.component';
import { CustomerContactComponent } from './customer/customer-contact/customer-contact.component';
import { BeneficiaryComponent } from './admin/beneficiary/beneficiary.component';
import { DonationComponent } from './admin/donation/donation.component';
import { DonationParticipantComponent } from './admin/donation-participant/donation-participant.component';
import { CustomerServiceComponent } from './customer/customer-service/customer-service.component';
import { StatistiqueComponent } from './admin/statistique/statistique.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    CustomerLayoutComponent,
    CustomerHeaderComponent,
    CustomerFooterComponent,
    LoginComponent,

    AuthenticationLayoutComponent,

    AdminLayoutComponent,
    DashboardComponent,
    AdminHeaderComponent,
    AdminMenuComponent,
    AdminFooterComponent,
    EventTypeComponent,
    LogoutComponent,
    EventComponent,
    ContributionComponent,
    UserComponent,
    UserProfileComponent,
    ContactComponent,
    MessageComponent,
    RegulationComponent,
    NewsComponent,
    SettingComponent,
    ForgotPasswordComponent,
    ResetPasswordComponent,
    RegisterComponent,
    AproposComponent,
    CustomerContactComponent,
    BeneficiaryComponent,
    DonationComponent,
    DonationParticipantComponent,
    CustomerServiceComponent,
    StatistiqueComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    RouterModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    RecaptchaModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
