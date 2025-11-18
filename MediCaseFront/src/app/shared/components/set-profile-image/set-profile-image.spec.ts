import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SetProfileImage } from './set-profile-image';

describe('SetProfileImage', () => {
  let component: SetProfileImage;
  let fixture: ComponentFixture<SetProfileImage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SetProfileImage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SetProfileImage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
