import { Component } from '@angular/core';
import { NewsService } from 'src/app/core/services/news/news.service';
import { SettingService } from 'src/app/core/services/setting/setting.service';
import { News } from 'src/app/core/models/News';
import { AuthService } from 'src/app/core/services/authentication/auth.service';
import { Title } from '@angular/platform-browser';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  all_news: News[] = [];
  error: string = '';

  $setting = this.settingService.setting$;

  constructor(
    private titleService: Title,
    private newsService: NewsService,
    private settingService: SettingService,
    private auth: AuthService
  ) {
    this.settingService.setting$.subscribe(setting => {
      if (setting?.nameApp) {
        this.titleService.setTitle(`Accueil | ${setting.nameApp}`);
      }
    });
  }

  ngOnInit() {
    this.auth.logout();
    this.fetchNews();
  }

  fetchNews(): void {

      this.newsService.getAllNews().subscribe({
        next: (data) => {
          this.all_news = data;
        },
        error: err => this.error = err.message
      });
    }

  selectedImage: string | null = null;

  openImage(photo: string): void {
      this.selectedImage = 'http://127.0.0.1:8080/uploads/' + photo;
  }

  closeImage(): void {
      this.selectedImage = null;
  }
}
