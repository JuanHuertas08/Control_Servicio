import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';

import { OrdenServicioService } from './orden-servicio';

describe('OrdenServicioService', () => {
  let service: OrdenServicioService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(OrdenServicioService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
