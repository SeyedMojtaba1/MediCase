import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TSideBar } from './t-side-bar';

describe('TSideBar', () => {
  let component: TSideBar;
  let fixture: ComponentFixture<TSideBar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TSideBar]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TSideBar);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
