import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SectionPageS } from './section-page-s';

describe('SectionPageS', () => {
  let component: SectionPageS;
  let fixture: ComponentFixture<SectionPageS>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SectionPageS]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SectionPageS);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
