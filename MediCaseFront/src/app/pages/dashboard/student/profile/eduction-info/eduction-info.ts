import {Component} from '@angular/core';
import {Card} from '../../../../../layouts/card/card';
import {InputText} from 'primeng/inputtext';
import {Password} from 'primeng/password';

@Component({
  selector: 'app-eduction-info',
  imports: [
    Card,
    InputText,
    Password
  ],
  templateUrl: './eduction-info.html',
  styleUrl: './eduction-info.css'
})
export class EductionInfo {

}
