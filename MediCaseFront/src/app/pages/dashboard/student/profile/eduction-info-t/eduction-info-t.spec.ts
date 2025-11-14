import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EductionInfoT } from './eduction-info-t';

describe('EductionInfoT', () => {
  let component: EductionInfoT;
  let fixture: ComponentFixture<EductionInfoT>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EductionInfoT]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EductionInfoT);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
