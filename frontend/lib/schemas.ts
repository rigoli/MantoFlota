import { z } from "zod";

export const estadoUnidadSchema = z.enum(["activa", "taller", "baja"]);

export const unidadCreateSchema = z.object({
  numero_economico: z.string().min(1),
  placas: z.string().min(1),
  marca: z.string().min(1),
  modelo: z.string().min(1),
  anio: z.coerce.number().min(1900).max(2100),
  tipo_vehiculo: z.string().min(1),
  kilometraje_actual: z.coerce.number().int().min(0),
  estado: estadoUnidadSchema,
});

export const unidadEditSchema = unidadCreateSchema.partial();

export const kilometrajeSchema = z.object({
  kilometraje_actual: z.coerce.number().int().min(0),
});

export const mantenimientoSchema = z.object({
  tipo: z.string().min(1),
  fecha_servicio: z.string().min(1),
  kilometraje: z.coerce.number().int().min(0),
  costo: z.coerce.number().min(0),
  proveedor: z.string().min(1),
  observaciones: z.string().optional().nullable(),
  responsable: z.string().min(1),
});
