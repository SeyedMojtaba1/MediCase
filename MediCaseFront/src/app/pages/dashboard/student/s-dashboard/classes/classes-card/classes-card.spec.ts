import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClassesCard } from './classes-card';

describe('ClassesCard', () => {
  let component: ClassesCard;
  let fixture: ComponentFixture<ClassesCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClassesCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ClassesCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
