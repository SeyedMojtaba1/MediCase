import {Component, Input} from '@angular/core';
import {Card} from '../../../layouts/card/card';
import {NgClass} from '@angular/common';


interface Player {
  rank: number;
  name: string;
  score: number;
}


@Component({
  selector: 'app-top',
  imports: [
    Card,
    NgClass
  ],
  templateUrl: './top.html',
  styleUrl: './top.css'
})
export class Top {

  @Input() showname = false
  @Input() count = 5
  @Input() mode!: number;
  @Input() subject = ''


  myName = 'علی (شما)'; // اسم کاربر فعلی
  showCount = this.count

  players: Player[] = [
    {rank: 1, name: 'سمیرا', score: 43},
    {rank: 2, name: 'محسن', score: 40},
    {rank: 3, name: 'عرشیا', score: 34},
    {rank: 4, name: 'محمد', score: 33},
    {rank: 5, name: 'مرتضی', score: 31},
    {rank: 6, name: 'مهسا', score: 30},
    {rank: 64, name: 'علی (شما)', score: 20},
  ];

  get topPlayers() {
    return this.players.slice(0, this.showCount);
  }

  get myPlayer() {
    return this.players.find(p => p.name === this.myName);
  }

}
