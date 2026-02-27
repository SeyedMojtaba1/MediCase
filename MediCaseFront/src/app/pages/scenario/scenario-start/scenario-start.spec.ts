import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScenarioStart } from './scenario-start';

describe('ScenarioStart', () => {
  let component: ScenarioStart;
  let fixture: ComponentFixture<ScenarioStart>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScenarioStart]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ScenarioStart);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
