import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubjectIntro } from './subject-intro';

describe('SubjectIntro', () => {
  let component: SubjectIntro;
  let fixture: ComponentFixture<SubjectIntro>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubjectIntro]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SubjectIntro);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
