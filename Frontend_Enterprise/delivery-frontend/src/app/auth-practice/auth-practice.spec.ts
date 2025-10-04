import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AuthPractice } from './auth-practice';

describe('AuthPractice', () => {
  let component: AuthPractice;
  let fixture: ComponentFixture<AuthPractice>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AuthPractice]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AuthPractice);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
