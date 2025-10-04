import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LogUploadComponent } from './log-file';

describe('LogFile', () => {
  let component: LogUploadComponent;
  let fixture: ComponentFixture<LogUploadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LogUploadComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LogUploadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
