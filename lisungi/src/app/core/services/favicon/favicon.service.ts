import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FaviconService {

  setFavicon(url: string): void {

    // Supprimer tous les anciens favicons
    document
      .querySelectorAll('link[rel="icon"], link[rel="shortcut icon"]')
      .forEach(link => link.remove());

    // Créer le nouveau favicon
    const link = document.createElement('link');

    link.rel = 'icon';
    link.type = 'image/png';
    link.href = url;

    document.head.appendChild(link);

    console.log('Favicon appliqué :', link.href);
    console.log(
      'Favicons présents :',
      document.querySelectorAll('link[rel="icon"]')
    );
  }
}
