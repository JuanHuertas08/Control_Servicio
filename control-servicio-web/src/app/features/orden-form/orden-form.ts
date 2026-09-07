import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { catchError, debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { of } from 'rxjs';

import { ClienteService } from '../../core/services/cliente';
import { OrdenServicioService } from '../../core/services/orden-servicio';
import { Cliente } from '../../core/models/cliente.model';
import { OrdenServicio } from '../../core/models/orden-servicio.model';

@Component({
  selector: 'app-orden-form',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './orden-form.html',
  styleUrl: './orden-form.scss',
})
export class OrdenForm {
  private fb = inject(FormBuilder);
  private clienteService = inject(ClienteService);
  private ordenService = inject(OrdenServicioService);

  cliente = signal<Cliente | null>(null);
  clienteNoEncontrado = signal(false);
  buscandoCliente = signal(false);
  guardando = signal(false);
  mensaje = signal<string | null>(null);
  error = signal<string | null>(null);

  form = this.fb.group({
    nit: ['', Validators.required],
    centro: ['', Validators.required],
    centro_beneficio: ['', Validators.required],
    pssr: ['', Validators.required],
    pedido: [null as number | null, Validators.required],
    factura: [''],
    tipo_doc: ['', Validators.required],
    unidad: ['', Validators.required],
    marca: ['', Validators.required],
    fecha_documento: ['', Validators.required],
    fecha_entrega: [''],
    venta_neta: [0, [Validators.required, Validators.min(0)]],
    gross_margin: [0, [Validators.required, Validators.min(0)]],
    margen_porcentaje: [0, Validators.required],
    repuestos: [0],
    mano_obra: [0],
    terceros: [0],
  });

  clienteForm = this.fb.group({
    razon_social: ['', Validators.required],
    telefono: [''],
    email: ['', Validators.email],
    direccion: [''],
    ciudad: [''],
    contacto: [''],
  });

  constructor() {
    this.form.controls.nit.valueChanges
      .pipe(debounceTime(400), distinctUntilChanged(), takeUntilDestroyed())
      .subscribe((nit) => this.buscarCliente(nit ?? ''));
  }

  buscarCliente(nitCrudo: string) {
    const nit = nitCrudo.trim();
    this.cliente.set(null);
    this.clienteNoEncontrado.set(false);
    this.mensaje.set(null);
    this.clienteForm.reset();

    if (!nit) {
      return;
    }

    this.buscandoCliente.set(true);
    this.clienteService
      .buscarPorNit(nit)
      .pipe(
        catchError(() => {
          this.clienteNoEncontrado.set(true);
          return of(null);
        }),
      )
      .subscribe((cliente) => {
        this.buscandoCliente.set(false);
        this.cliente.set(cliente);
        if (cliente) {
          this.clienteForm.patchValue(cliente);
        }
      });
  }

  registrarCliente() {
    if (this.clienteForm.invalid) {
      this.clienteForm.markAllAsTouched();
      return;
    }

    const nit = (this.form.controls.nit.value ?? '').trim();
    const datos = this.clienteForm.getRawValue();
    const nuevoCliente: Cliente = {
      nit,
      razon_social: datos.razon_social ?? '',
      telefono: datos.telefono || null,
      email: datos.email || null,
      direccion: datos.direccion || null,
      ciudad: datos.ciudad || null,
      contacto: datos.contacto || null,
    };

    this.clienteService.crear(nuevoCliente).subscribe({
      next: (cliente) => {
        this.cliente.set(cliente);
        this.clienteNoEncontrado.set(false);
        this.mensaje.set('Cliente registrado en el maestro.');
      },
      error: () => this.error.set('No se pudo registrar el cliente. Verifica los datos.'),
    });
  }

  guardarOrden() {
    this.error.set(null);
    this.mensaje.set(null);

    if (this.form.invalid || !this.cliente()) {
      this.form.markAllAsTouched();
      this.error.set('Completa los datos obligatorios y confirma el cliente por su NIT.');
      return;
    }

    this.guardando.set(true);
    const valores = this.form.getRawValue();
    const orden: OrdenServicio = {
      ...valores,
      nit: (valores.nit ?? '').trim(),
      pedido: Number(valores.pedido),
      factura: valores.factura || null,
      fecha_entrega: valores.fecha_entrega || null,
    } as OrdenServicio;

    this.ordenService.crear(orden).subscribe({
      next: () => {
        this.guardando.set(false);
        this.mensaje.set('Orden de servicio creada correctamente.');
        this.form.reset({ venta_neta: 0, gross_margin: 0, margen_porcentaje: 0, repuestos: 0, mano_obra: 0, terceros: 0 });
        this.clienteForm.reset();
        this.cliente.set(null);
      },
      error: (err) => {
        this.guardando.set(false);
        this.error.set(err?.error?.nit?.[0] ?? 'No se pudo guardar la orden de servicio.');
      },
    });
  }
}
