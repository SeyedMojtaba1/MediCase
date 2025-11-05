import {Component, Input} from '@angular/core';
import {Card} from '../../../../../layouts/card/card';
import {NgClass} from '@angular/common';
import {RouterLink} from '@angular/router';


@Component({
  selector: 'app-hospital-card',
  imports: [
    Card,
    NgClass,
    RouterLink
  ],
  templateUrl: './hospital-card.html',
  styleUrl: './hospital-card.css'
})
export class HospitalCard {
  @Input() sub: any
}
