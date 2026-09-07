import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { OrdenServicio } from '../models/orden-servicio.model';

@Injectable({
  providedIn: 'root',
})
export class OrdenServicioService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiUrl}/ordenes`;

  listar(): Observable<OrdenServicio[]> {
    return this.http.get<OrdenServicio[]>(`${this.baseUrl}/`);
  }

  crear(orden: OrdenServicio): Observable<OrdenServicio> {
    return this.http.post<OrdenServicio>(`${this.baseUrl}/`, orden);
  }
}
