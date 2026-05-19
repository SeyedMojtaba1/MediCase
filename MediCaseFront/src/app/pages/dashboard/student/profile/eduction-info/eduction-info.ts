import {ChangeDetectorRef, Component, Input} from '@angular/core';
import {Card} from '../../../../../layouts/card/card';
import {InputText} from 'primeng/inputtext';

@Component({
  selector: 'app-eduction-info',
  imports: [
    Card,
    InputText
  ],
  templateUrl: './eduction-info.html',
  styleUrl: './eduction-info.css'
})
export class EductionInfo {
  @Input() user: any

  constructor(public changeDetector: ChangeDetectorRef) {


  }

  ngOnInit() {
    console.log(this.user);
    this.changeDetector.detectChanges()
  }
}
