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
    errorMessage = '';
    selectedNews!: News;

    publicId: any;

    statusInfo = true;

    newsForm!: FormGroup;
    selectedFile!: File;
    currentSettingId: number | null = null;
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

    initForm() {
      this.newsForm = this.fb.group({
        title: ['', Validators.required],
        content: ['', Validators.required]
      });
    }

    private showModal(id: string) {
      $('#' + id).modal('show');
    }

    private hideModal(id: string) {
      $('#' + id).modal('hide');
    }

    openDeleteModal(news: any) {
        this.selectedNews = news;
        this.showModal('deleteModal');
    }

    deleteNews(publicId: string){

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }
      this.newsService.deleteNews(publicId).subscribe({
        next: () =>{
            this.hideModal('deleteModal');
            this.fetchNews();
        },
        error: err => this.error = err.message
      });
    }

    fetchNews(): void {

      this.newsService.getAllNews().subscribe({
        next: (data) => {
          this.all_news = data;
        },
        error: err => this.error = err.message
      });
    }

    onFileSelected(event: any) {
      if (event.target.files.length > 0) {
        this.selectedFile = event.target.files[0];

        const reader = new FileReader();
        reader.onload = () => {
          this.photoPreview = reader.result as string;
        };
        reader.readAsDataURL(this.selectedFile);
      }
    }

    openAddModal(){
      this.errorMessage = '';
      this.initForm();
      this.showModal('addNewsModal');
    }

    addNews(){

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }

      this.errorMessage = '';

      const formData = new FormData();

      formData.append(
        'data',
        new Blob([JSON.stringify(this.newsForm.value)], { type: 'application/json' })
      );

      if (this.selectedFile) {
        formData.append('photo', this.selectedFile);
      }

      this.newsService.addNews(formData).subscribe({
        next: () => {
          this.initForm();
          this.statusInfo = true;
          this.fetchNews();
          this.showModal('infoModal');
        },
        error: (err) => {
          console.log(err);
          this.errorMessage = err.error;
        }
      });
    }

    openUpdateModal(publicId: string){

      this.errorMessage = '';

      this.newsService.getNews(publicId).subscribe({
        next: (data) => {
          this.publicId = data.publicId;
          this.photoPreview = data.photo!;

          this.newsForm = this.fb.group({
            title: data.title,
            content: data.content
          });

          this.showModal('updateNewsModal');
        },
        error: err => this.error = err.message
      })
    }

    updNews() {

      if (!this.authService.isAdmin()) {
        this.errorMessage = 'Vous n’avez pas les droits nécessaires.';
        return;
      }

      this.errorMessage = '';

      const formData = new FormData();

      formData.append(
        'data',
        new Blob([JSON.stringify(this.newsForm.value)], { type: 'application/json' })
      );

      if (this.selectedFile) {
        formData.append('photo', this.selectedFile);
      }

      this.newsService.updateNews(this.publicId, formData).subscribe({
        next: () => {
          this.statusInfo = false;
          this.fetchNews();
          this.showModal('infoModal');
        },
        error: (err) => {
          console.log(err);
          this.errorMessage = err.error;
        }
      });
    }
}
