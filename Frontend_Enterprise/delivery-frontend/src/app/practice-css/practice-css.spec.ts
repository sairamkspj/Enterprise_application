import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PracticeCss } from './practice-css';

describe('PracticeCss', () => {
  let component: PracticeCss;
  let fixture: ComponentFixture<PracticeCss>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PracticeCss]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PracticeCss);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
