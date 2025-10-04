import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardComp } from './dashboard-comp';

describe('DashboardComp', () => {
  let component: DashboardComp;
  let fixture: ComponentFixture<DashboardComp>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashboardComp]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DashboardComp);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
