import {Component, Input} from '@angular/core';
import {Card} from '../../../../../layouts/card/card';
import {RouterLink} from '@angular/router';
import {NgClass} from '@angular/common';


@Component({
  selector: 'app-hospital-card',
  imports: [
    Card,
    RouterLink,
    NgClass
  ],
  templateUrl: './hospital-card.html',
  styleUrl: './hospital-card.css'
})
export class HospitalCard {
  @Input() sub: any
  @Input() active: boolean = false;


}
