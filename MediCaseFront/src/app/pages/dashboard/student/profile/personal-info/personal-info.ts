import {ChangeDetectorRef, Component, Input, signal} from '@angular/core';
import {Card} from '../../../../../layouts/card/card';
import {InputText} from 'primeng/inputtext';
import {FormsModule} from '@angular/forms';
import {InputGroup} from 'primeng/inputgroup';
import {Button} from 'primeng/button';
import {ChangeLogin} from '../../../../../shared/components/change-login/change-login';

@Component({
  selector: 'app-personal-info',
  imports: [
    Card,
    InputText,
    FormsModule,
    InputGroup,
    Button,
    ChangeLogin
  ],
  templateUrl: './personal-info.html',
  styleUrl: './personal-info.css'
})
export class PersonalInfo {
  a1 = 'asfdasdfs'
  isChangeOpen = signal(false)
  @Input() user: any
  visible: boolean = false;
  protected readonly alert = alert;
  protected readonly console = console;
  protected readonly ChangeLogin = ChangeLogin;

  constructor(public changeDetectorRef: ChangeDetectorRef) {
  }

  ngOnInit(): void {
    this.changeDetectorRef.detectChanges();
  }

  openChangeLogin() {
    this.isChangeOpen.set(true);
    this.visible = true;
    this.changeDetectorRef.detectChanges(); // درست، چون اینجا context صحیح است
  }
}
