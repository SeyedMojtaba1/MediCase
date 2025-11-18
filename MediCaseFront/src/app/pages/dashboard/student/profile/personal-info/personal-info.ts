import {ChangeDetectorRef, Component, Input} from '@angular/core';
import {Card} from '../../../../../layouts/card/card';
import {InputText} from 'primeng/inputtext';
import {FormsModule} from '@angular/forms';
import {InputGroup} from 'primeng/inputgroup';
import {Button} from 'primeng/button';

@Component({
  selector: 'app-personal-info',
  imports: [
    Card,
    InputText,
    FormsModule,
    InputGroup,
    Button
  ],
  templateUrl: './personal-info.html',
  styleUrl: './personal-info.css'
})
export class PersonalInfo {
  a1 = 'asfdasdfs'
  @Input() user: any

  constructor(public changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit(): void {
    this.changeDetectorRef.detectChanges();
  }
}
