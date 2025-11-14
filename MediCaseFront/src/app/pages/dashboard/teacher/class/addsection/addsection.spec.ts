import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Addsection } from './addsection';

describe('Addsection', () => {
  let component: Addsection;
  let fixture: ComponentFixture<Addsection>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Addsection]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Addsection);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
