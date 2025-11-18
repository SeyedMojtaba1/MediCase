import {ChangeDetectorRef, Component} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Master} from '../../core/services/master';
import {DashNavT} from '../components/dash-nav-t/dash-nav-t';
import confetti from 'canvas-confetti';
import {Card} from '../../layouts/card/card';


@Component({
  selector: 'app-public-profile',
  imports: [
    DashNavT,
    Card
  ],
  templateUrl: './public-profile.html',
  styleUrl: './public-profile.css'
})
export class PublicProfile {

  user: any
  id = ''

  constructor(private route: ActivatedRoute, public master: Master, public changeDetectorRef: ChangeDetectorRef) {
  }

  fireConfetti() {
    confetti({
      particleCount: 150,
      spread: 80,
      origin: {y: 0.6}
    });
  }

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id')!;

    this.master.user(this.id).subscribe({
      next: (result: any) => {
        console.log(result);
        this.user = result.body;
      },
      complete: () => {
        this.changeDetectorRef.detectChanges();
      }
    })
  }

}
