import { describe, expect, it } from "vitest";

import { mantenimientoSchema, unidadCreateSchema } from "@/lib/schemas";

describe("schemas", () => {
  it("valida unidad mínima", () => {
    const r = unidadCreateSchema.safeParse({
      numero_economico: "A",
      placas: "X",
      marca: "M",
      modelo: "Mo",
      anio: 2024,
      tipo_vehiculo: "Van",
      kilometraje_actual: 0,
      estado: "activa",
    });
    expect(r.success).toBe(true);
  });

  it("rechaza kilometraje negativo", () => {
    const r = unidadCreateSchema.safeParse({
      numero_economico: "A",
      placas: "X",
      marca: "M",
      modelo: "Mo",
      anio: 2024,
      tipo_vehiculo: "Van",
      kilometraje_actual: -1,
      estado: "activa",
    });
    expect(r.success).toBe(false);
  });

  it("valida mantenimiento", () => {
    const r = mantenimientoSchema.safeParse({
      tipo: "P",
      fecha_servicio: "2026-04-19",
      kilometraje: 1,
      costo: 10,
      proveedor: "Pr",
      responsable: "Re",
    });
    expect(r.success).toBe(true);
  });
});
