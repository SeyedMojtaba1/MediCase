import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders, HttpResponse} from '@angular/common/http';
import {Router} from '@angular/router';
import {Observable} from 'rxjs';
import {APP_CONFIG} from '../../config/app.config';

@Injectable({
  providedIn: 'root',
})
export class Master {
  BASE_URL = APP_CONFIG.baseURL;

  constructor(
    private http: HttpClient,
    private router: Router,) {
  }

  login(email: string, password: string): Observable<HttpResponse<any>> {
    return this.http.post<any>(
      this.BASE_URL + 'register/login',
      {
        email: email,
        password: password,
      },
      {observe: 'response'},
    );
  }

  signup(
    username: string,
    email: string,
    password: string,
  ): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({'Content-Type': 'application/json'});

    return this.http.post<any>(
      this.BASE_URL + 'register/signup',
      {
        email: email,
        password: password,
        name: username,
      },
      {
        headers,
        observe: 'response',
      },
    );
  }

  buycoin(coin: number): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    });

    return this.http.get(
      'https://sang-e-saboor-production.ir/registery/buycoin/?coin=' + coin,
      {headers, observe: 'response'},
    );
  }
}
