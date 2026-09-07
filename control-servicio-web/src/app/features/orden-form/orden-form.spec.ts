import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';

import { OrdenForm } from './orden-form';

describe('OrdenForm', () => {
  let component: OrdenForm;
  let fixture: ComponentFixture<OrdenForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrdenForm],
      providers: [provideHttpClient(), provideHttpClientTesting()],
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrdenForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
