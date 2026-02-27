import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SectionPageT } from './section-page-t';

describe('SectionPageT', () => {
  let component: SectionPageT;
  let fixture: ComponentFixture<SectionPageT>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SectionPageT]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SectionPageT);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
