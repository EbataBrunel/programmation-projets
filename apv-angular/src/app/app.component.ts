import { Component } from '@angular/core';
import { environment } from './environments/environment';
import { SettingService } from './core/services/setting/setting.service';
import { AuthService } from './core/services/authentication/auth.service';
import { FaviconService } from './core/services/favicon/favicon.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'apv';

  private rootUrl = `${environment.apiUrl}/uploads`;

  constructor(
    private settingService: SettingService,
    private faviconService: FaviconService,
    private authService: AuthService
  ) {
    this.settingService.setting$.subscribe(setting => {

      if (setting?.logo) {
        const logoUrl =
          `${this.rootUrl}/${setting.logo}`;

        this.faviconService.setFavicon(logoUrl);
      }

    });
  }

  ngOnInit(): void {
    this.settingService.loadSetting().subscribe({
      error: err => console.error('Erreur lors du chargement du paramètre', err)
    });
    /** Restaurer l'utilisateur au démarrage */
    if (this.authService.isAuthenticated()) {

      this.authService.restoreCurrentUser();

    }
  }
}
