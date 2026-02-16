import {Component, Input} from '@angular/core';
import {Card} from '../../../../../layouts/card/card';
import {InputText} from 'primeng/inputtext';

@Component({
  selector: 'app-eduction-info-t',
  imports: [
    Card,
    InputText
  ],
  templateUrl: './eduction-info-t.html',
  styleUrl: './eduction-info-t.css'
})
export class EductionInfoT {
  @Input() user: any

  ngOnInit() {
  }
}
