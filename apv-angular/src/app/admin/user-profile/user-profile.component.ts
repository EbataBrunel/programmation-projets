import { Component } from '@angular/core';
import { NgForm } from '@angular/forms';
import { UserProfileService } from 'src/app/core/services/userProfile/user-profile.service';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ChangePasswordRequest } from 'src/app/core/models/ChangePasswordRequest';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { UserProfileReasonRemoval } from 'src/app/core/models/UserProfileReasonRemoval';
import { UserProfile } from 'src/app/core/models/UserProfile';
import { Reason } from 'src/app/core/models/Reason';
import { Title } from '@angular/platform-browser';

declare var $: any;

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent {
  user: any
  setting: any;
  profile!: UserProfile;
  publicId!: string;
  info!: string;

  userProfileReasonRemoval: UserProfileReasonRemoval = {
    reasonRemoval: null
  };

  countries: any[] = [
                'Afrique du Sud',
                'Afghanistan',
                'Albanie',
                'Allemagne',
                'Andorre',
                'Angola',
                'Antigua-et-Barbuda',
                'Arabie Saoudite',
                'Argentine',
                'Arménie',
                'Australie',
                'Autriche',
                'Azerbaïdjan',
                'Bahamas',
                'Bahreïn',
                'Bangladesh',
                'Barbade',
                'Belgique',
                'Belize',
                'Bénin',
                'Bhoutan',
                'Biélorussie',
                'Birmanie',
                'Bolivie',
                'Bosnie-Herzégovine',
                'Botswana',
                'Brésil',
                'Brunei',
                'Bulgarie',
                'Burkina Faso',
                'Burundi',
                'Cambodge',
                'Cameroun',
                'Canada',
                'Cap-Vert',
                'Chili',
                'Chine',
                'Chypre',
                'Colombie',
                'Comores',
                'Congo-Brazzaville',
                'Corée du Nord',
                'Corée du Sud',
                'Costa Rica	San',
                'Côte d’Ivoire',
                'Croatie',
                'Cuba',
                'Danemark',
                'Djibouti',
                'Dominique',
                'Égypte',
                'Émirats arabes unis',
                'Équateur',
                'Érythrée',
                'Espagne',
                'Eswatini',
                'Estonie',
                'États-Unis',
                'Éthiopie',
                'Fidji',
                'Finlande',
                'France',
                'Gabon',
                'Gambie',
                'Géorgie',
                'Ghana',
                'Grèce',
                'Grenade',
                'Guatemala',
                'Guinée',
                'Guinée équatoriale',
                'Guinée-Bissau',
                'Guyana',
                'Haïti',
                'Honduras',
                'Hongrie',
                'Îles Cook',
                'Îles Marshall',
                'Inde',
                'Indonésie',
                'Irak',
                'Iran',
                'Irlande',
                'Islande',
                'Israël',
                'Italie',
                'Jamaïque',
                'Japon',
                'Jordanie',
                'Kazakhstan',
                'Kenya',
                'Kirghizistan',
                'Kiribati',
                'Koweït',
                'Laos',
                'Lesotho',
                'Lettonie',
                'Liban',
                'Liberia',
                'Libye',
                'Liechtenstein',
                'Lituanie',
                'Luxembourg',
                'Macédoine',
                'Madagascar',
                'Malaisie',
                'Malawi',
                'Maldives',
                'Mali',
                'Malte',
                'Maroc',
                'Maurice',
                'Mauritanie',
                'Mexique',
                'Micronésie',
                'Moldavie',
                'Monaco',
                'Mongolie',
                'Monténégro',
                'Mozambique',
                'Namibie',
                'Nauru',
                'Népal',
                'Nicaragua',
                'Niger',
                'Nigeria',
                'Niue',
                'Norvège',
                'Nouvelle-Zélande',
                'Oman',
                'Ouganda',
                'Ouzbékistan',
                'Pakistan',
                'Palaos',
                'Palestine',
                'Panama',
                'Papouasie-Nouvelle-Guinée',
                'Paraguay',
                'Pays-Bas',
                'Pérou',
                'Philippines',
                'Pologne',
                'Portugal',
                'Qatar',
                'République centrafricaine',
                'République démocratique du Congo',
                'République Dominicaine',
                'République tchèque',
                'Roumanie',
                'Royaume-Uni',
                'Russie',
                'Rwanda',
                'Saint-Kitts-et-Nevis',
                'Saint-Vincent-et-les-Grenadines',
                'Sainte-Lucie',
                'Saint-Marin',
                'Salomon',
                'Salvador',
                'Samoa',
                'São Tomé-et-Principe',
                'Sénégal',
                'Serbie',
                'Seychelles',
                'Sierra Leone',
                'Singapour',
                'Slovaquie',
                'Slovénie',
                'Somalie',
                'Soudan',
                'Soudan du Sud',
                'Sri Lanka',
                'Suède',
                'Suisse',
                'Suriname',
                'Syrie',
                'Tadjikistan',
                'Tanzanie',
                'Tchad',
                'Thaïlande',
                'Timor oriental',
                'Togo',
                'Tonga',
                'Trinité-et-Tobago',
                'Tunisie',
                'Turkménistan',
                'Turquie',
                'Tuvalu',
                'Ukraine',
                'Uruguay',
                'Vanuatu',
                'Vatican',
                'Venezuela',
                'Viêt Nam',
                'Yémen',
                'Zambie',
                'Zimbabwe'
  ];

  genders: string[] = ["MASCULIN", "FEMININ"];
  reasons: Reason[] = [
  {
    value: 'JE_NE_SUIS_PLUS_INTERESSE',
    label: 'Je ne suis plus intéressé'
  },
  {
    value: 'JE_NE_SUIS_PLUS_DISPONIBLE',
    label: 'Je ne suis plus disponible'
  },
  {
    value: 'ORGANISATION_N_EST_PAS_BONNE',
    label: "L'organisation n'est pas bonne"
  },
  {
    value: 'AUTRES',
    label: "Autres"
  }
];

  passwordForm!: FormGroup
  errorMessage = '';
  error = '';

  setting$ = this.settingService.setting$;
  isAdmin$ = this.authService.isAdmin$;
  isSupAdmin$ = this.authService.isSupAdmin$;

  constructor(
    private fb: FormBuilder,
    private titleService: Title,
    private auth: AuthService,
    private profileService: UserProfileService,
    private settingService: SettingService,
    private authService: AuthService
  ){
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Profiles | ${setting.nameApp}`);
      }
    });
  }

  ngOnInit() {
    // Charger l'utilisateur connecté
    this.getCurrentUser();
    this.initForm();

  }

  private showModal(id: string) {
    $('#' + id).modal('show');
  }

  private hideModal(id: string) {
    $('#' + id).modal('hide');
  }

  getCurrentUser(){
    this.auth.getCurrentUser().subscribe({
        next: (data) => {
            this.user = data;
            this.profileService.getProfileByUser(data.publicId).subscribe(
              (profileuser) => {
                this.profile = profileuser;
              }
            );
        },
        error: (err) => console.error(err)
    });
  }

  initForm(){
    this.passwordForm = this.fb.group({
      oldPassword: ['', Validators.required],
      newPassword: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', Validators.required]
    });
  }

  openProfileModal(){
    this.info = '';
    this.showModal('openProfileModal');
  }

  updateUserProfile(){
    this.profileService.updateUserProfile(this.profile).subscribe({
      next: (data) => {

        this.profile = data;
        this.info = 'Profil modifié avec succès.';
        // récupérer le nouveau profile
        this.profileService.setProfile(data);
        $("#infoModal").modal("show");
      },
      error: err => this.error = err.message
    })
  }

  openPhotoModal(){
    this.showModal('photo-modal');
  }

  replaceImage(event: any){

      const file = event.target.files[0];
      if(!file) return;

      const formData = new FormData();
      formData.append('photo', file);
      this.profileService.updateUserPhoto(this.profile.publicId!, formData).subscribe({
        next: (newProfile) => {

          // Profile mise à jour
          this.profile = newProfile;

          // récupérer le nouveau profile
          this.profileService.setProfile(newProfile);

        },
        error: err => this.error = err.message
      });
    }

    openChangePasswordModal(){
      this.initForm();
      this.showModal('openChangePasswordModal');
    }

    changePassword() {

      this.errorMessage = '';

      if (this.passwordForm.invalid) {
        return;
      }

      this.auth.changePassword(this.passwordForm.value as ChangePasswordRequest)
        .subscribe({
          next: () => {
            alert("Mot de passe modifié avec succès");
            this.passwordForm.reset();
            this.hideModal('openChangePasswordModal');
          },
          error: (err) => {
            this.errorMessage = err.error;
          }
        });

    }

  openReasonRemovalModal(publicId: string) {

    this.publicId = publicId;

    // Toujours ouvrir le formulaire vide
    this.userProfileReasonRemoval = {
      reasonRemoval: null
    };

    this.showModal('openReasonRemovalModal');
  }


  updateReasonRemoval(form: NgForm) {

    this.info = '';

    if (form.invalid) {
      return;
    }

    this.profileService.updateReasonRemoval(
      this.publicId,
      this.userProfileReasonRemoval
    ).subscribe({

      next: (userProfile) => {

        console.log(
          'Profil mis à jour :',
          userProfile
        );

        this.getCurrentUser();

        this.info =
          'Raison de suppression de compte enregistrée avec succès.';

        // Réinitialise le formulaire Angular
        form.resetForm();

        // Réinitialise également le modèle
        this.userProfileReasonRemoval = {
          reasonRemoval: null
        };

        $("#infoModal").modal("show");
      },

      error: (err) => {
        console.error(err);
        this.error = err.message;
      }

    });
  }

}
