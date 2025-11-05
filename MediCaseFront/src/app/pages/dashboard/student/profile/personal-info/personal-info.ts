import {Component} from '@angular/core';
import {Card} from '../../../../../layouts/card/card';
import {InputText} from 'primeng/inputtext';
import {Password} from 'primeng/password';
import {FormsModule} from '@angular/forms';
import {InputGroup} from 'primeng/inputgroup';
import {Button} from 'primeng/button';

@Component({
  selector: 'app-personal-info',
  imports: [
    Card,
    InputText,
    Password,
    FormsModule,
    InputGroup,
    Button
  ],
  templateUrl: './personal-info.html',
  styleUrl: './personal-info.css'
})
export class PersonalInfo {
  a1 = 'asdfasdf'
}
