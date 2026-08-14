import { Component } from '@angular/core';
import { ChangeDetectorRef } from '@angular/core';
import { UserService } from 'src/app/core/services/user/user.service';
import { ViewService } from 'src/app/core/services/view/view.service';
import { UserProfileService } from 'src/app/core/services/userProfile/user-profile.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { User } from 'src/app/core/models/User';
import { Role } from 'src/app/core/models/Role';
import { View } from 'src/app/core/models/View';
import { UserProfile } from 'src/app/core/models/UserProfile';
import { DATATABLE_FR } from 'src/app/core/config/datatable-fr';
import { Title } from '@angular/platform-browser';

declare var $: any;

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styles: [
  ]
})
export class UserComponent {
    roles: Role[] = [];
    all_roles: Role[] = [];
    error: string = '';
    users: User[] = [];
    profiles: UserProfile[] = [];
    views:  View[] = [];
    roleNames = ["ROLE_SUPADMIN", "ROLE_ADMIN", "ROLE_CUSTOMER", "ALL"];
    days = ["Today", "Remove", "Other"];
    nameUser!: string;
    roleName!: string;
    day!: string
    selectedDetailUser: Partial<User> = {};

    userPublicId!: string;
    profilePublicId!: string;
    statusInfo!: string;

    countSupAdmin = 0;
    countAdmin = 0;
    countCustomer = 0;
    countAllUser = 0;
    countViews = 0;
    countNewsRegistrations = 0;
    countProfiles = 0;

    setting$ = this.settingService.setting$;
    isAdmin$ = this.authService.isAdmin$;
    isSupAdmin$ = this.authService.isSupAdmin$;
    currentUser$ = this.authService.currentUser$;

    constructor(
      private titleService: Title,
      private cdr: ChangeDetectorRef,
      private userService: UserService,
      private profileService: UserProfileService,
      private viewService: ViewService,
      private settingService: SettingService,
      private authService: AuthService
    ) {
      this.settingService.setting$.subscribe(setting => {
        if (setting?.nameApp) {
          this.titleService.setTitle(`Utilisateurs | ${setting.nameApp}`);
        }
      });
    }

    ngOnInit(){
      this.getAllRoles();
      this.getCountUsers();
      this.getCountViews();
      this.getCountTodayRegistrations();
      this.getViewdByAdminIdAndStatusFalse();
      this.loadProfilesByReasonRemovalNot();
    }

    private showModal(id: string) {
      $('#' + id).modal('show');
    }

    private hideModal(id: string) {
      $('#' + id).modal('hide');
    }

    isCurrentUser(user: User, currentUser: User | null): boolean {
      return user.publicId === currentUser?.publicId;
    }

    getCountUsers(){
      this.userService.getUsers().subscribe({
        next: (data) => {
          const users = data ?? [];
          this.countSupAdmin = data.filter(user =>user.roles?.some(role => role.name === "ROLE_SUPADMIN")).length;
          this.countAdmin = data.filter(user =>user.roles?.some(role => role.name === "ROLE_ADMIN")).length;
          this.countCustomer = data.filter(user =>user.roles?.some(role => role.name === "ROLE_CUSTOMER")).length;
          this.countAllUser = users.length;
        },
        error: (err) => console.error(err)
      });
    }

    openUserModal(roleName: string): void {

      if (roleName == "ALL"){
        this.roleName = roleName;

        this.loadAllUsers();
      }else{
        this.roleName = roleName;
        // Charger les utilisateur du rôle selectionné
        this.loadUsers();
      }
    }

    loadAllUsers(){

      if ($.fn.DataTable.isDataTable('#example1')) {
          $('#example1').DataTable().destroy();
      }

      this.userService.getUsers().subscribe({
        next: (data) => {

          this.users = data

          this.cdr.detectChanges();

          $('#example1').DataTable({
              language: DATATABLE_FR,
              destroy: true
          });

          this.showModal('userModal');
        },
        error: (err) => console.error(err)
      });
    }

    loadUsers(){

      if ($.fn.DataTable.isDataTable('#example1')) {
          $('#example1').DataTable().destroy();
        }

        this.userService.getUsers().subscribe({
          next: (data) => {

            this.users = data.filter(user =>
              user.roles?.some(role => role.name === this.roleName)
            );

            this.cdr.detectChanges();

            $('#example1').DataTable({
              language: DATATABLE_FR,
              destroy: true
            });

            this.showModal('userModal');
          },
          error: (err) => console.error(err)
        });
    }

    openRegistrationModal(day: string): void {

      if (day == "Today"){

        this.day = day;

        if ($.fn.DataTable.isDataTable('#registrationsTable')) {
          $('#registrationsTable').DataTable().destroy();
        }

        this.profileService.getTodayRegistrations().subscribe({
          next: (data) => {

            this.profiles = data;

            this.cdr.detectChanges();

            $('#registrationsTable').DataTable({
              language: DATATABLE_FR,
              destroy: true
            });

            this.showModal('registrationModal');
          },
          error: (err) => console.error(err)
        });
      }else if (day == "Remove"){
        this.day = day;

        if ($.fn.DataTable.isDataTable('#registrationsTable')) {
          $('#registrationsTable').DataTable().destroy();
        }

        this.profileService.getProfilesByReasonRemovalNot().subscribe({
          next: (data) => {

            this.profiles = data;

            this.cdr.detectChanges();

            $('#registrationsTable').DataTable({
              language: DATATABLE_FR,
              destroy: true
            });

            this.showModal('registrationModal');
          },
          error: (err) => console.error(err)
        });
      }else{

        this.day = day;

        if ($.fn.DataTable.isDataTable('#registrationsTable')) {
          $('#registrationsTable').DataTable().destroy();
        }

        this.viewService.createMissingViews().subscribe({

          next: (count) => {

            this.getViewdByAdminIdAndStatusFalse();

            this.cdr.detectChanges();

            $('#registrationsTable').DataTable({
              language: DATATABLE_FR,
              destroy: true
            });

            this.showModal('registrationModal');
          },
          error: (err) => console.error(err)
        });
      }
    }

    // Ouvrir la la modal de prise de prise de décison de la suppression de compte d'un memebre
    openResponseReasonRemovalModal(profile: UserProfile) {

      this.profilePublicId = profile.publicId!;
      // Récuperer le membre à supprimer
      this.userService.getUserById(profile.userId).subscribe({
        next: (user)  => {
          this.selectedDetailUser = user;
          this.showModal('openResponseReasonRemovalModal');
        },
        error: (err) => console.error(err)
      });

    }

    updateDecisionReasonRemoval() {
        const userProfileReasonRemoval = {
          reasonRemoval: 'JE_SUIS_INTERESSE'
        }
        this.profileService.updateReasonRemoval(
          this.profilePublicId,
          userProfileReasonRemoval).subscribe({

          next: (up) => {
            this.statusInfo = 'La décision de la suppression du compte prise avec succès.'
            this.loadProfilesByReasonRemovalNot();
            this.hideModal('openResponseReasonRemovalModal');
            $("#infoModal").modal("show");
          },

          error: (err) => {
            console.error(err);
            this.error = err.message;
          }

        });
    }

    getAllRoles(){
      this.userService.getAllRoles().subscribe({
        next: (data) => {
          this.all_roles = data;
        },
        error: (err) => console.error(err)
      })
    }

    getRoles(userPublicId: string) {
      this.userService.getUser(userPublicId).subscribe({
        next: (data) => {
          this.userPublicId = data.publicId!;
          this.nameUser = data.userProfile.lastName+" "+data.userProfile.firstName;
          this.roles = data.roles ?? [];
          this.showModal('roleModal');
        },
        error: (err) => console.error(err)
      });
    }

    detailUser(user: User) {
      this.selectedDetailUser = user;
      this.showModal('detailModal');
    }

    openDeleteUserModal(user: User){
      this.selectedDetailUser = user;
      this.showModal('deleteUserModal');
    }

    deleteUser(publicId: string){
      this.userService.deleteUser(publicId).subscribe({
        next: () => {
          if (this.roleName === "ALL"){
            this.loadAllUsers();
          }else{
            this.loadUsers();
          }
          this.getCountUsers();
          this.statusInfo = "Utilisateur supprimé avec succès";
          this.showModal('infoModal');
        },
        error: (err) => console.error(err)
      });
    }

    openDeleteRoleToUserModal(roleName: string){
      this.roleName = roleName;
      this.showModal('deleteRoleToUserModal');
    }

    deleteRoleToUser(roleName: string){
      this.userService.removeRoleToUser(this.userPublicId, roleName).subscribe({
        next: (data) => {
          this.getRoles(data.publicId!);
          this.getCountUsers();
          this.hideModal('deleteRoleToUserModal');
          this.statusInfo = "Role suprimé à l'utilisateur avec succès";
          this.showModal('infoModal');
        },
        error: (err) => console.log(err)
      })
    }

    openAddRoleToUserModal() {
      this.showModal('adRoleToUserModal');
    }

    addRoleToUser(roleName: string): void {

      this.userService.addRoleToUser(this.userPublicId, roleName).subscribe({
        next: (user) => {
          this.getRoles(user.publicId!)
          this.getCountUsers();
          this.statusInfo = "Rôle ajouté à l'utilisateur avec succès";
          this.showModal('infoModal');
        },
        error: (err) => console.error(err)
      });
    }

    closeModal(){
      this.viewService.updateStatusView().subscribe({
        next: (result) => {
          this.getViewdByAdminIdAndStatusFalse();
          this.hideModal("registrationModal");
        },
        error: (err) => console.error(err)
      })
    }

    getViewdByAdminIdAndStatusFalse(){
      this.viewService.getViewsByAdmin().subscribe({
            next: (data) => this.views = data,
            error: (err) => console.log(err)
      });
    }

    getCountViews(){
      this.viewService.getCountUsersNotViewWithAdmin().subscribe({
        next: (count)  => {
          this.countViews = count;
        },
        error: err => this.error = err.message
      })
    }

    getCountTodayRegistrations(){
      this.profileService.getTodayRegistrations().subscribe({
        next: (data) => {

          this.countNewsRegistrations = data.length;
        },
        error: (err) => console.log(err)
      });
    }

    loadProfilesByReasonRemovalNot(){
      this.profileService.getProfilesByReasonRemovalNot().subscribe({
        next: (data) => {
          this.countProfiles = data.length;
        },
        error: (error) => {
          console.error('Erreur lors de la récupération des profils', error);
        }
      });
    }
}
