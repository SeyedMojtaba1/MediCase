import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SSideBar } from './s-side-bar';

describe('SSideBar', () => {
  let component: SSideBar;
  let fixture: ComponentFixture<SSideBar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SSideBar]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SSideBar);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
