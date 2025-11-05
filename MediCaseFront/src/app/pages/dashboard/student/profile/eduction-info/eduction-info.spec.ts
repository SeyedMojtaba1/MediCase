import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EductionInfo } from './eduction-info';

describe('EductionInfo', () => {
  let component: EductionInfo;
  let fixture: ComponentFixture<EductionInfo>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EductionInfo]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EductionInfo);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
