/** Tipos alineados con la API FastAPI (/api/v1). */

export type EstadoUnidad = "activa" | "taller" | "baja";

export interface Unidad {
  id: number;
  numero_economico: string;
  placas: string;
  marca: string;
  modelo: string;
  anio: number;
  tipo_vehiculo: string;
  kilometraje_actual: number;
  estado: EstadoUnidad;
  creado_en: string;
  actualizado_en: string;
}

export type RolUsuario = "administrador" | "operador" | "consulta";

export interface UsuarioMe {
  id: number;
  email: string;
  nombre: string;
  rol: RolUsuario;
}

export interface Mantenimiento {
  id: number;
  unidad_id: number;
  tipo: string;
  fecha_servicio: string;
  kilometraje: number;
  costo: number;
  proveedor: string;
  observaciones: string | null;
  responsable: string;
  creado_en: string;
  actualizado_en: string;
}

/** Fila en listado global ``GET /api/v1/mantenimientos``. */
export interface MantenimientoListItem extends Mantenimiento {
  numero_economico: string;
  placas: string;
}

/** ``GET /api/v1/dashboard/inicio`` — estimaciones por heurística (último servicio +90 d / +10 000 km). */
export interface ProximoMantenimientoRow {
  unidad_id: number;
  numero_economico: string;
  placas: string;
  marca: string;
  modelo: string;
  ultima_fecha_servicio: string | null;
  ultimo_kilometraje_en_servicio: number | null;
  kilometraje_actual: number;
  proxima_fecha_estimada: string;
  proximo_kilometraje_estimado: number;
}

/** Unidades con estado taller (pendientes de salir). */
export interface UnidadEnTallerRow {
  unidad_id: number;
  numero_economico: string;
  placas: string;
  marca: string;
  modelo: string;
  kilometraje_actual: number;
  actualizado_en: string;
}

export interface DashboardInicio {
  proximos_mantenimientos: ProximoMantenimientoRow[];
  unidades_en_taller: UnidadEnTallerRow[];
}
