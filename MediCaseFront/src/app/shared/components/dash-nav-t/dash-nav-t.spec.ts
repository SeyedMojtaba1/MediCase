import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashNavT } from './dash-nav-t';

describe('DashNavT', () => {
  let component: DashNavT;
  let fixture: ComponentFixture<DashNavT>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashNavT]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DashNavT);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
