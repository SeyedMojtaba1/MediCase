import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChangeLogin } from './change-login';

describe('ChangeLogin', () => {
  let component: ChangeLogin;
  let fixture: ComponentFixture<ChangeLogin>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChangeLogin]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChangeLogin);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
