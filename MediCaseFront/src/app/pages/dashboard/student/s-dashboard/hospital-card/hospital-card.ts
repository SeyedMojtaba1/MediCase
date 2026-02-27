import {Component} from '@angular/core';
import {RouterLink} from '@angular/router';
import {NgStyle} from '@angular/common';

@Component({
  selector: 'app-hospital-card',
  imports: [
    RouterLink,
    NgStyle
  ],
  templateUrl: './hospital-card.html',
  styleUrl: './hospital-card.css'
})
export class HospitalCard {
  public image = "images/svg/hospital.svg"

}
