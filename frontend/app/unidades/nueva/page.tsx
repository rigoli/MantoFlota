"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import type { z } from "zod";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import * as api from "@/lib/api";
import { unidadCreateSchema } from "@/lib/schemas";

type FormValues = z.infer<typeof unidadCreateSchema>;

export default function NuevaUnidadPage() {
  const router = useRouter();
  const form = useForm<FormValues>({
    resolver: zodResolver(unidadCreateSchema),
    defaultValues: {
      numero_economico: "",
      placas: "",
      marca: "",
      modelo: "",
      anio: new Date().getFullYear(),
      tipo_vehiculo: "",
      kilometraje_actual: 0,
      estado: "activa",
    },
  });

  async function onSubmit(values: FormValues) {
    try {
      const u = await api.createUnidad(values);
      toast.success("Unidad registrada");
      router.push(`/unidades/${u.id}`);
    } catch (e) {
      toast.error((e as Error).message);
    }
  }

  return (
    <div className="mx-auto w-full max-w-xl">
      <Card>
        <CardHeader>
          <CardTitle>Nueva unidad</CardTitle>
          <CardDescription>
            Completa los datos. El kilometraje debe ser mayor o igual a cero.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form
            className="space-y-4"
            onSubmit={form.handleSubmit(onSubmit)}
          >
            <div className="grid gap-2">
              <Label htmlFor="numero_economico">Número económico</Label>
              <Input
                id="numero_economico"
                {...form.register("numero_economico")}
              />
              {form.formState.errors.numero_economico && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.numero_economico.message}
                </p>
              )}
            </div>
            <div className="grid gap-2">
              <Label htmlFor="placas">Placas</Label>
              <Input id="placas" {...form.register("placas")} />
              {form.formState.errors.placas && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.placas.message}
                </p>
              )}
            </div>
            <div className="grid gap-2 sm:grid-cols-2">
              <div className="grid gap-2">
                <Label htmlFor="marca">Marca</Label>
                <Input id="marca" {...form.register("marca")} />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="modelo">Modelo</Label>
                <Input id="modelo" {...form.register("modelo")} />
              </div>
            </div>
            <div className="grid gap-2 sm:grid-cols-2">
              <div className="grid gap-2">
                <Label htmlFor="anio">Año</Label>
                <Input
                  id="anio"
                  type="number"
                  {...form.register("anio", { valueAsNumber: true })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="tipo_vehiculo">Tipo de vehículo</Label>
                <Input id="tipo_vehiculo" {...form.register("tipo_vehiculo")} />
              </div>
            </div>
            <div className="grid gap-2">
              <Label htmlFor="kilometraje_actual">Kilometraje actual</Label>
              <Input
                id="kilometraje_actual"
                type="number"
                {...form.register("kilometraje_actual", {
                  valueAsNumber: true,
                })}
              />
              {form.formState.errors.kilometraje_actual && (
                <p className="text-sm text-destructive">
                  {form.formState.errors.kilometraje_actual.message}
                </p>
              )}
            </div>
            <div className="grid gap-2">
              <Label>Estado</Label>
              <Select
                value={form.watch("estado") ?? "activa"} // eslint-disable-line react-hooks/incompatible-library
                onValueChange={(v) =>
                  form.setValue("estado", v as FormValues["estado"])
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder="Estado" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="activa">Activa</SelectItem>
                  <SelectItem value="taller">Taller</SelectItem>
                  <SelectItem value="baja">Baja</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button type="submit" disabled={form.formState.isSubmitting}>
              Guardar unidad
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
