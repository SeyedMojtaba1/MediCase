import { Component, signal } from '@angular/core';
import {APP_CONFIG} from './config/app.config';
import {RouterOutlet} from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  a!:any;
  protected readonly title = signal('MediCaseFront');
  ngOnInit() {
    this.a= APP_CONFIG.theme.colors.backgroundGradient;

  }

  protected readonly APP_CONFIG = APP_CONFIG;
}
