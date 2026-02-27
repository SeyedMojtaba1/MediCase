import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TDashboard } from './t-dashboard';

describe('TDashboard', () => {
  let component: TDashboard;
  let fixture: ComponentFixture<TDashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TDashboard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TDashboard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
