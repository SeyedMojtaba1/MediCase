import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SDashboard } from './s-dashboard';

describe('SDashboard', () => {
  let component: SDashboard;
  let fixture: ComponentFixture<SDashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SDashboard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SDashboard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
