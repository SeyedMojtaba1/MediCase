import {ChangeDetectorRef, Component} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {DashNav} from '../../../../../shared/components/dash-nav/dash-nav';

@Component({
  selector: 'app-select',
  imports: [
    DashNav
  ],
  templateUrl: './select.html',
  styleUrl: './select.css'
})
export class Select {

  subject = ''

  constructor(public route: ActivatedRoute, public changeDetector: ChangeDetectorRef) {
  }

  ngOnInit() {
    this.subject = this.route.snapshot.paramMap.get('sub')!;
  }


  getSubjectText(): string {
    switch (this.subject) {
      case 'Pulmonology':
        return 'سلام';
      case 'b':
        return 'خب';
      case 'c':
        return 'خوش آمدید';
      default:
        return 'مقدار نامعتبر';
    }
  }
}
