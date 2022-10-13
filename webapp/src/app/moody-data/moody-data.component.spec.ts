import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MoodyDataComponent } from './moody-data.component';

describe('MoodyDataComponent', () => {
  let component: MoodyDataComponent;
  let fixture: ComponentFixture<MoodyDataComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MoodyDataComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MoodyDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
