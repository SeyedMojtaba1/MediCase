import {Component, ElementRef, signal} from '@angular/core';
import {APP_CONFIG} from './config/app.config';
import {NavigationEnd, Router, RouterOutlet} from '@angular/router';
import {Toast} from 'primeng/toast';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    Toast,
  ],
  templateUrl: './app.html',
  styleUrl: './app.css',
  standalone: true,
})
export class App {
  a!: any;
  protected readonly title = signal('MediCaseFront');
  protected readonly APP_CONFIG = APP_CONFIG;


  constructor(public router: Router, private el: ElementRef) {
  }


  ngOnInit() {
    this.a = APP_CONFIG.theme.colors.backgroundGradient;


    this.router.events.subscribe((event) => {
      if (!(event instanceof NavigationEnd)) {
        return;
      }
      window.scrollTo(0, 0)
    });

  }


}
