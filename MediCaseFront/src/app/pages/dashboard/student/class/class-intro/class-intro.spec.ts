import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassIntro } from './class-intro';

describe('ClassIntro', () => {
  let component: ClassIntro;
  let fixture: ComponentFixture<ClassIntro>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassIntro]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ClassIntro);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
