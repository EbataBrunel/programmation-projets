import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CountryService {
  private apiUrl = 'https://restcountries.com/api/v1/all?fields=name,cca2,flags';

  constructor(private http: HttpClient) {}

  getCountries(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl).pipe(
      map(countries =>
        countries
          .map(c => ({
            name: c.name.common,
            code: c.cca2,
            flag: c.flags?.svg
          }))
          .sort((a, b) => a.name.localeCompare(b.name))
      )
    );
  }
}
