import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Cliente } from '../models/cliente.model';

@Injectable({
  providedIn: 'root',
})
export class ClienteService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiUrl}/clientes`;

  buscarPorNit(nit: string): Observable<Cliente> {
    return this.http.get<Cliente>(`${this.baseUrl}/${nit}/`);
  }

  buscar(q: string): Observable<Cliente[]> {
    return this.http.get<Cliente[]>(`${this.baseUrl}/`, { params: { q } });
  }

  crear(cliente: Cliente): Observable<Cliente> {
    return this.http.post<Cliente>(`${this.baseUrl}/`, cliente);
  }
}
