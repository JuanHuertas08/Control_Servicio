export interface OrdenServicio {
  id?: number;
  centro: string;
  centro_beneficio: string;
  pssr: string;
  pedido: number;
  factura?: string | null;
  tipo_doc: string;
  nit: string;
  cliente_nit?: string;
  cliente_nombre?: string;
  unidad: string;
  marca: string;
  fecha_documento: string;
  fecha_entrega?: string | null;
  venta_neta: number;
  gross_margin: number;
  margen_porcentaje: number;
  repuestos: number;
  mano_obra: number;
  terceros: number;
}
