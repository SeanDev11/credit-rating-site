import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SandpDataComponent } from './sandp-data.component';

describe('SandpDataComponent', () => {
  let component: SandpDataComponent;
  let fixture: ComponentFixture<SandpDataComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SandpDataComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SandpDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
