import {Component} from '@angular/core';
import {Card} from 'primeng/card';
import {Button} from 'primeng/button';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-not-found404',
  imports: [
    Card,
    Button,
    RouterLink
  ],
  templateUrl: './not-found404.html',
  styleUrl: './not-found404.css'
})
export class NotFound404 {

  protected readonly localStorage = localStorage;
}
