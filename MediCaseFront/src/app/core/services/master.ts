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
    return this.http.post<any>(
      this.BASE_URL + 'registery/logout/',
      {refresh: localStorage.getItem('refresh_token')},
      {
        headers,
        observe: 'response',
        withCredentials: true,
      },
    );
  }

  refresh(): Observable<HttpResponse<any>> {
    return this.http.post<any>(
      this.BASE_URL + 'registery/token/refresh/',
      {refresh: localStorage.getItem('refresh_token')},
      {
        headers: new HttpHeaders({
          'Content-Type': 'application/json',
        }),
        observe: 'response',
        withCredentials: true,
      }
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

  setProfileImage(file: File): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    const formData = new FormData();
    formData.append('profile_image', file);

    return this.http.put<any>(
      this.BASE_URL + '/registery/setprofileimage/',
      formData,
      {
        headers,
        observe: 'response',
        withCredentials: true,
      }
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


  // ***************************************************************************
  // ***************************************************************************
  //                              subject
  // ***************************************************************************
  // ***************************************************************************
  // اینجا اطلاعات بیماری ها، لیست رشته ها ، دروس و بیمارستان های قابل انتخاب میاد

  createSection(data: any): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });
    return this.http.post<any>(this.BASE_URL + 'class/sectioncreate/', {
      name: data.name,
      subject_name: data.subject,
      semester_code: data.semester_code,
      start_date: data.start_date,
      end_date: data.end_date,
      description: data.description,
    }, {
      headers,
      observe: 'response',
      withCredentials: true
    },)
  }

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

    return this.http.get<any>(this.BASE_URL + 'class/sectionlist/', {
      headers,
      observe: 'response',
      withCredentials: true
    });
  }

  semesters(): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'class/semesters/', {
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

  user(id: any): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'registery/users/' + id + "/", {
      headers,
      observe: 'response',
      withCredentials: true
    });
  }

  sectionRetrieve(id: any): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'class/sectionretrieve/' + id + '/', {
      headers,
      observe: 'response',
      withCredentials: true
    });
  }

  memberSectionList(id: any): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'class/memberssectiontlist/' + id + '/', {
      headers,
      observe: 'response',
      withCredentials: true
    });
  }

  addStudent(section: any, student: any): Observable<HttpResponse<any>> {

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.post<any>(this.BASE_URL + 'class/studentsectioncreate/', {
      section: section,
      student: student,
      student_status: "Active"
    }, {
      headers,
      observe: 'response',
      withCredentials: true
    });

  }

  sectionUpdate(data: any): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });
    return this.http.put<any>(this.BASE_URL + 'class/sectionupdate/' + data.sectionID + '/', {
      new_name: data.new_name,
      semester_code: data.semester_code,
      start_date: data.start_date,
      end_date: data.end_date,
      description: data.description,
    }, {
      headers,
      observe: 'response',
      withCredentials: true
    },)
  }

  studentSubjectList(): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'class/studentsubjectlist/', {
      headers,
      observe: 'response',
      withCredentials: true
    });
  }

  selectHospital(id: any): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'class/hospitalsubjectretrieve/' + id + '/', {
      headers,
      observe: 'response',
      withCredentials: true
    });
  }


  // ***************************************************************************
  // ***************************************************************************
  //                              scenario
  // ***************************************************************************
  // ***************************************************************************
  // اینجا اطلاعات بیماری ها، لیست رشته ها ، دروس و بیمارستان های قابل انتخاب میاد
  // pulmonologyscenario


  pulmonologyScenarioCreate(): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'pulmonologyscenario/scenariocreate/', {
      headers,
      observe: 'response',
      withCredentials: true
    });
  }

  pulmonologyScenarioRetrieve(tracking_code: any): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'pulmonologyscenario/scenarioretrieve/' + tracking_code + '/', {
      headers,
      withCredentials: true
    });
  }

  pulmonologyScenarioFeedbackRetrieve(tracking_code: any): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'pulmonologyscenario/feedbackretrieve/' + tracking_code + '/', {
      headers,
      withCredentials: true
    });
  }

  pulmonologyScenarioFeedbackCreate(tracking_code: any, log: any): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.post<any>(this.BASE_URL + 'pulmonologyscenario/feedbackcreate/' + tracking_code,
      {student_log: log}
      , {
        headers,
        withCredentials: true
      });
  }


  scenarioList(): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + '/pulmonologyscenario/scenariolist/' + localStorage.getItem('personal_number') + '/', {
      headers,
      withCredentials: true
    });
  }

  feedbackList(): Observable<HttpResponse<any>> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    })
    return this.http.get<any>(this.BASE_URL + '/pulmonologyscenario/feedbacklist/' + localStorage.getItem('personal_number') + '/', {
      headers,
      withCredentials: true
    })
  }

  // ***************************************************************************
// ***************************************************************************
//                              hospital
// ***************************************************************************
// ***************************************************************************
// لیست بیمارستانا


  hospitalSubject(subject: string): Observable<HttpResponse<any>> {

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'class/hospitalsubjectretrieve/' + subject + '/', {
      headers,
      withCredentials: true
    });

  }


  hospitalInfo(name: string): Observable<HttpResponse<any>> {

    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    });

    return this.http.get<any>(this.BASE_URL + 'class/hospitals/' + name + '/', {
      headers,
      withCredentials: true
    });

  }

}




