import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashNav } from './dash-nav';

describe('DashNav', () => {
  let component: DashNav;
  let fixture: ComponentFixture<DashNav>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashNav]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DashNav);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
