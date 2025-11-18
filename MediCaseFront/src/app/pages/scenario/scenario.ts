import {Component} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {APP_CONFIG} from '../../config/app.config';
import {NgClass} from '@angular/common';

interface Disease {
  name: string;
  checked: boolean;
}

interface Section {
  id: number;
  title: string;
  icon: string;
}

interface Question {
  id: number;
  title: string;
  answer: string;
  open: boolean;
  visible: boolean;
}


@Component({
  selector: 'app-scenario',
  imports: [
    FormsModule,
    NgClass
  ],
  templateUrl: './scenario.html',
  styleUrl: './scenario.css'
})
export class Scenario {

  logo = APP_CONFIG.logoURL;
  backgroundImage = 'assets/bg.jpg';

  diseases: Disease[] = [];
  sections: Section[] = [];
  activeSection: number | null = null;


  clickSound = new Audio('sounds/click.mp3');
  successSound = new Audio('sounds/success.mp3');
  questions: Question[] = [];
  protected readonly APP_CONFIG = APP_CONFIG;

  ngOnInit() {
    this.loadDiseases();
    this.loadSections();


    this.questions = [
      {id: 1, title: 'علائم بیماری چیست؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 2, title: 'علت بیماری چیست؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 3, title: 'درمان چیه؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 1, title: 'علائم بیماری چیست؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 2, title: 'علت بیماری چیست؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 3, title: 'درمان این بیماری چرا و چگونه چیه؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 1, title: 'علائم بیماری چیست؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 2, title: 'علت بیماری چیست؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 3, title: 'درمان چیه؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 1, title: 'علائم بیماری چیست؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 2, title: 'علت بیماری چیست؟', answer: 'پاسخ نمونه...', open: false, visible: false},
      {id: 3, title: 'درمان چیه؟', answer: 'پاسخ نمونه...', open: false, visible: false},
    ];
  }

  playClick() {
    this.clickSound.currentTime = 0;
    this.clickSound.play();
  }

  playSuccess() {
    this.successSound.currentTime = 0;
    this.successSound.play();
  }

  loadDiseases() {
    this.diseases = [
      {name: 'Asthma', checked: false},
      {name: 'Pneumonia', checked: false},
    ];
  }

  loadSections() {
    this.sections = [
      {id: 1, title: 'اطلاعات بیمار', icon: 'pi pi-id-card'},
      {id: 2, title: 'شرح حال', icon: 'pi pi-list'},
      {id: 3, title: 'معاینه', icon: 'pi pi-heart'},
      {id: 4, title: 'پاراکلینیک', icon: 'pi pi-folder'},
      {id: 5, title: 'تشخیص افتراقی', icon: 'pi pi-pencil'},
      {id: 6, title: 'درمان', icon: 'pi pi-lock'},
    ];
  }

  selectSection(section: Section) {
    this.activeSection = section.id;
    // this.playSuccess();
  }

  toggleQuestion(q: any) {
    if (!q.visible) {
      q.visible = true;
      this.playSuccess()
    } else {
      q.open = !q.open;
      this.playClick()
    }
  }

}
