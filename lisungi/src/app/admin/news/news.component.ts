import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { NewsService } from 'src/app/core/services/news/news.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { News } from 'src/app/core/models/News';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { Title } from '@angular/platform-browser';

declare var $: any;

@Component({
  selector: 'app-news',
  templateUrl: './news.component.html',
  styles: [
  ]
})
export class NewsComponent {

  roles: string[] = [];
  all_news: News[] = [];

  error: string = '';
  errorMessage: string = '';

  selectedNews!: News;

  publicId: string | undefined = undefined;

  statusInfo = true;

  newsForm!: FormGroup;

  // Fichier sélectionné pour Cloudinary
  selectedFile?: File;

  currentSettingId: number | null = null;

  // URL Cloudinary ou data:image/... pour la prévisualisation
  photoPreview: string = '';

  setting$ = this.settingService.setting$;
  isAdmin$ = this.authService.isAdmin$;

  constructor(
    private fb: FormBuilder,
    private titleService: Title,
    private newsService: NewsService,
    private settingService: SettingService,
    private authService: AuthService
  ) {

    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Actualités | ${setting.nameApp}`);
      }
    });

  }

  ngOnInit(): void {
    this.initForm();
    this.fetchNews();
  }

  /**
   * Initialisation du formulaire
   */
  initForm(): void {
    this.newsForm = this.fb.group({
      title: ['', Validators.required],
      content: ['', Validators.required]
    });
  }

  /**
   * Afficher une modal Bootstrap
   */
  private showModal(id: string): void {
    $('#' + id).modal('show');
  }

  /**
   * Fermer une modal Bootstrap
   */
  private hideModal(id: string): void {
    $('#' + id).modal('hide');
  }

  /**
   * Ouvrir la modal de suppression
   */
  openDeleteModal(news: News): void {
    this.selectedNews = news;
    this.showModal('deleteModal');
  }

  /**
   * Supprimer une actualité
   */
  deleteNews(publicId: string): void {

    if (!this.authService.isAdmin()) {
      this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
      return;
    }

    this.errorMessage = '';

    this.newsService.deleteNews(publicId).subscribe({

      next: () => {
        this.hideModal('deleteModal');
        this.fetchNews();
      },

      error: (err) => {
        console.error('Erreur suppression news :', err);

        this.errorMessage =
          err?.error?.message ||
          err?.error ||
          'Erreur lors de la suppression de l’actualité.';
      }

    });
  }

  /**
   * Récupérer toutes les actualités
   */
  fetchNews(): void {

    this.newsService.getAllNews().subscribe({

      next: (data) => {
        this.all_news = data;
      },

      error: (err) => {
        console.error('Erreur récupération news :', err);
        this.error = err.message;
      }

    });
  }

  /**
   * Sélection d'une photo
   *
   * La photo est conservée dans selectedFile.
   * La prévisualisation utilise une data URL.
   */
  onFileSelected(event: Event): void {

    const input = event.target as HTMLInputElement;

    if (!input.files || input.files.length === 0) {
      return;
    }

    this.selectedFile = input.files[0];

    this.errorMessage = '';

    const reader = new FileReader();

    reader.onload = () => {
      this.photoPreview = reader.result as string;
    };

    reader.onerror = () => {
      this.errorMessage = 'Impossible de prévisualiser la photo.';
    };

    reader.readAsDataURL(this.selectedFile);
  }

  /**
   * Ouvrir la modal d'ajout
   */
  openAddModal(): void {

    this.errorMessage = '';

    // Très important :
    // on oublie le fichier sélectionné précédemment
    this.selectedFile = undefined;

    // On supprime l'ancienne prévisualisation
    this.photoPreview = '';

    // Réinitialisation du formulaire
    this.initForm();

    this.showModal('addNewsModal');
  }

  /**
   * Ajouter une actualité
   */
  addNews(): void {

    if (!this.authService.isAdmin()) {
      this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
      return;
    }

    if (this.newsForm.invalid) {
      this.newsForm.markAllAsTouched();
      return;
    }

    this.errorMessage = '';

    const formData = new FormData();

    /**
     * Partie JSON envoyée au backend
     */
    formData.append(
      'data',
      new Blob(
        [JSON.stringify(this.newsForm.value)],
        {
          type: 'application/json'
        }
      )
    );

    /**
     * Partie fichier.
     *
     * Le backend envoie ensuite ce fichier à Cloudinary.
     */
    if (this.selectedFile) {
      formData.append(
        'photo',
        this.selectedFile,
        this.selectedFile.name
      );
    }

    this.newsService.addNews(formData).subscribe({

      next: (data) => {

        console.log('Actualité créée :', data);

        this.initForm();

        this.selectedFile = undefined;
        this.photoPreview = '';

        this.statusInfo = true;

        this.fetchNews();

        this.hideModal('addNewsModal');

        this.showModal('infoModal');
      },

      error: (err) => {

        console.error('Erreur ajout news :', err);

        this.errorMessage =
          err?.error?.message ||
          err?.error ||
          'Erreur lors de l’ajout de l’actualité.';
      }

    });
  }

  /**
   * Ouvrir la modal de modification
   */
  openUpdateModal(publicId: string): void {

    this.errorMessage = '';

    // Très important :
    // on ne doit pas conserver une ancienne photo
    this.selectedFile = undefined;

    this.newsService.getNews(publicId).subscribe({

      next: (data) => {

        console.log('Actualité récupérée :', data);

        this.publicId = data.publicId;

        /**
         * Si la photo existe, elle doit maintenant être
         * une URL Cloudinary.
         *
         * Exemple :
         * https://res.cloudinary.com/...
         *
         * Si aucune photo :
         * ''
         */
        this.photoPreview = data.photo || '';

        /**
         * Formulaire de modification
         */
        this.newsForm = this.fb.group({
          title: [
            data.title,
            Validators.required
          ],

          content: [
            data.content,
            Validators.required
          ]
        });

        this.showModal('updateNewsModal');
      },

      error: (err) => {

        console.error(
          'Erreur récupération actualité :',
          err
        );

        this.errorMessage =
          err?.error?.message ||
          err?.error ||
          'Impossible de récupérer cette actualité.';
      }

    });
  }

  /**
   * Modifier une actualité
   */
  updNews(): void {

    if (!this.authService.isAdmin()) {
      this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
      return;
    }

    if (this.newsForm.invalid) {
      this.newsForm.markAllAsTouched();
      return;
    }

    if (!this.publicId) {
      this.errorMessage =
        'Identifiant de l’actualité introuvable.';
      return;
    }

    this.errorMessage = '';

    const formData = new FormData();

    /**
     * Partie JSON
     */
    formData.append(
      'data',
      new Blob(
        [JSON.stringify(this.newsForm.value)],
        {
          type: 'application/json'
        }
      )
    );

    /**
     * Nouvelle photo uniquement si l'utilisateur
     * en a sélectionné une.
     *
     * Si aucune nouvelle photo n'est sélectionnée,
     * le backend conserve l'ancienne URL Cloudinary.
     */
    if (this.selectedFile) {

      formData.append(
        'photo',
        this.selectedFile,
        this.selectedFile.name
      );
    }

    this.newsService.updateNews(
      this.publicId,
      formData
    ).subscribe({

      next: (data) => {

        console.log(
          'Actualité modifiée :',
          data
        );

        this.statusInfo = false;

        this.selectedFile = undefined;

        this.photoPreview = data.photo || '';

        this.fetchNews();

        this.hideModal('updateNewsModal');

        this.showModal('infoModal');
      },

      error: (err) => {

        console.error(
          'Erreur modification news :',
          err
        );

        this.errorMessage =
          err?.error?.message ||
          err?.error ||
          'Erreur lors de la modification de l’actualité.';
      }

    });
  }

}
