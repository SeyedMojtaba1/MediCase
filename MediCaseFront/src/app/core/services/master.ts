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


  // ***************************************************************************
  // ***************************************************************************
  //                                 registry
  // ***************************************************************************
  // ***************************************************************************

  constructor(
    private http: HttpClient,
    private router: Router,) {
  }

  login(email: string, password: string): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({'Content-Type': 'application/json'});

    return this.http.post<any>(
      this.BASE_URL + 'registery/login/',
      {
        email: email,
        password: password,
      },
      {observe: 'response', withCredentials: true},
    );
  }

  logout(): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });
    return this.http.get<any>(
      this.BASE_URL + 'registery/logout/',
      {
        headers,
        observe: 'response',
        withCredentials: true,
      },
    );
  }

  refresh(): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    return this.http.get<any>(
      this.BASE_URL + 'registery/token/refresh/',
      {
        headers,
        observe: 'response',
        withCredentials: true
      },
    );
  }

  sendOTP(email: string): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    return this.http.post<any>(this.BASE_URL + 'registery/sendresetotp/', {
      email: email,
    }, {observe: 'response', withCredentials: true},)
  }

  resetPass(email: string, pass: string): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    return this.http.post<any>(this.BASE_URL + 'registery/resetpass/', {
      email: email,
      new_password: pass,
    }, {observe: 'response', withCredentials: true},)
  }

  changePass(email: string): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    return this.http.post<any>(this.BASE_URL + 'registery/chengepass/', {
      "personal_number": "40127233",
      "password": "11111111",
      "new_password": "11111111@"
    }, {observe: 'response', withCredentials: true},)
  }

  verifyOTP(email: string, otp: string): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({'Content-Type': 'application/json'});
    return this.http.post<any>(this.BASE_URL + 'registery/verifyotp/', {
      "email": email,
      "otp": otp,
    }, {observe: 'response', withCredentials: true},)
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


  // ***************************************************************************
  // ***************************************************************************
  //                              subject
  // ***************************************************************************
  // ***************************************************************************
  // اینجا اطلاعات بیماری ها، لیست رشته ها ، دروس و بیمارستان های قابل انتخاب میاد

  subjectList(): Observable<HttpResponse<any>> {
    {
      const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      });

      return this.http.get<any>(this.BASE_URL + 'class/subjects/', {
        headers,
        observe: 'response',
        withCredentials: true
      });
    }
  }

  subjectDetail(subject: string): Observable<HttpResponse<any>> {
    {
      const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`,
      });

      return this.http.get<any>(this.BASE_URL + 'class/subjects/' + subject, {
        headers,
        observe: 'response',
        withCredentials: true
      });
    }
  }

  sections(): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'class/sections/', {
      headers,
      observe: 'response',
      withCredentials: true
    });
  }


  profile(): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'registery/userprofile/', {
      headers,
      observe: 'response',
      withCredentials: true
    });
  }
}
