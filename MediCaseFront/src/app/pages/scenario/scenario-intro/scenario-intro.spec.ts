import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScenarioIntro } from './scenario-intro';

describe('ScenarioIntro', () => {
  let component: ScenarioIntro;
  let fixture: ComponentFixture<ScenarioIntro>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScenarioIntro]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ScenarioIntro);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
