"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useRouter } from "next/navigation";
import * as React from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import type { z } from "zod";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Badge } from "@/components/ui/badge";
import { Button, buttonVariants } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";
import * as api from "@/lib/api";
import {
  kilometrajeSchema,
  mantenimientoSchema,
  unidadCreateSchema,
} from "@/lib/schemas";
import { cn } from "@/lib/utils";

type UnidadForm = z.infer<typeof unidadCreateSchema>;
type KmForm = z.infer<typeof kilometrajeSchema>;
type MantForm = z.infer<typeof mantenimientoSchema>;

export function UnidadClient({ id }: { id: number }) {
  const router = useRouter();
  const qc = useQueryClient();

  const uq = useQuery({
    queryKey: ["unidad", id],
    queryFn: () => api.getUnidad(id),
  });

  const mq = useQuery({
    queryKey: ["mantenimientos", id],
    queryFn: () => api.listMantenimientosPorUnidad(id),
    enabled: Number.isFinite(id),
  });

  const form = useForm<UnidadForm>({
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
    values: uq.data
      ? {
          numero_economico: uq.data.numero_economico,
          placas: uq.data.placas,
          marca: uq.data.marca,
          modelo: uq.data.modelo,
          anio: uq.data.anio,
          tipo_vehiculo: uq.data.tipo_vehiculo,
          kilometraje_actual: uq.data.kilometraje_actual,
          estado: uq.data.estado,
        }
      : undefined,
  });

  const kmForm = useForm<KmForm>({
    resolver: zodResolver(kilometrajeSchema),
    defaultValues: { kilometraje_actual: 0 },
  });

  const mantForm = useForm<MantForm>({
    resolver: zodResolver(mantenimientoSchema),
    defaultValues: {
      tipo: "",
      fecha_servicio: "",
      kilometraje: 0,
      costo: 0,
      proveedor: "",
      observaciones: "",
      responsable: "",
    },
  });

  React.useEffect(() => {
    if (uq.data) {
      kmForm.reset({ kilometraje_actual: uq.data.kilometraje_actual });
    }
  }, [uq.data, kmForm]);

  const saveUnidad = useMutation({
    mutationFn: (body: UnidadForm) => api.updateUnidad(id, body),
    onSuccess: async () => {
      toast.success("Unidad actualizada");
      await qc.invalidateQueries({ queryKey: ["unidad", id] });
      await qc.invalidateQueries({ queryKey: ["unidades"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  const saveKm = useMutation({
    mutationFn: (body: KmForm) =>
      api.patchKilometraje(id, body.kilometraje_actual),
    onSuccess: async () => {
      toast.success("Kilometraje actualizado");
      await qc.invalidateQueries({ queryKey: ["unidad", id] });
      await qc.invalidateQueries({ queryKey: ["unidades"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  const delUnidad = useMutation({
    mutationFn: () => api.deleteUnidad(id),
    onSuccess: async () => {
      toast.success("Unidad eliminada");
      await qc.invalidateQueries({ queryKey: ["unidades"] });
      router.push("/unidades");
    },
    onError: (e: Error) => toast.error(e.message),
  });

  const createMant = useMutation({
    mutationFn: (body: MantForm) =>
      api.createMantenimiento(id, {
        ...body,
        observaciones: body.observaciones?.trim()
          ? body.observaciones
          : null,
      }),
    onSuccess: async () => {
      toast.success("Mantenimiento registrado");
      mantForm.reset();
      await qc.invalidateQueries({ queryKey: ["mantenimientos", id] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  const delMant = useMutation({
    mutationFn: (mid: number) => api.deleteMantenimiento(mid),
    onSuccess: async () => {
      toast.success("Mantenimiento eliminado");
      await qc.invalidateQueries({ queryKey: ["mantenimientos", id] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  if (uq.isLoading) {
    return <p className="text-muted-foreground">Cargando unidad…</p>;
  }
  if (uq.isError || !uq.data) {
    return (
      <div className="space-y-4">
        <p className="text-destructive">
          No se pudo cargar la unidad: {(uq.error as Error)?.message}
        </p>
        <Link
          href="/unidades"
          className={cn(buttonVariants({ variant: "outline" }))}
        >
          Volver
        </Link>
      </div>
    );
  }

  const unidad = uq.data;
  const mantenimientos = mq.data ?? [];

  return (
    <div className="flex flex-col gap-8">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p className="text-sm text-muted-foreground">
            <Link href="/unidades" className="hover:underline">
              Unidades
            </Link>{" "}
            / {unidad.numero_economico}
          </p>
          <h1 className="mt-2 text-2xl font-semibold tracking-tight">
            {unidad.marca} {unidad.modelo}{" "}
            <Badge variant="outline">{unidad.estado}</Badge>
          </h1>
        </div>
        <div className="flex flex-wrap gap-2">
          <Dialog>
            <DialogTrigger
              render={
                <Button variant="secondary">Actualizar kilometraje</Button>
              }
            />
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Kilometraje</DialogTitle>
              </DialogHeader>
              <form
                className="space-y-4"
                onSubmit={kmForm.handleSubmit((v) => saveKm.mutate(v))}
              >
                <div className="grid gap-2">
                  <Label htmlFor="km">Nuevo kilometraje</Label>
                  <Input
                    id="km"
                    type="number"
                    {...kmForm.register("kilometraje_actual", {
                      valueAsNumber: true,
                    })}
                  />
                  {kmForm.formState.errors.kilometraje_actual && (
                    <p className="text-sm text-destructive">
                      {kmForm.formState.errors.kilometraje_actual.message}
                    </p>
                  )}
                </div>
                <DialogFooter>
                  <Button type="submit" disabled={saveKm.isPending}>
                    Guardar
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>

          <AlertDialog>
            <AlertDialogTrigger
              render={<Button variant="destructive">Eliminar unidad</Button>}
            />
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>¿Eliminar esta unidad?</AlertDialogTitle>
                <AlertDialogDescription>
                  Se borrarán todos los mantenimientos asociados.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancelar</AlertDialogCancel>
                <AlertDialogAction
                  className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                  onClick={() => delUnidad.mutate()}
                >
                  Eliminar
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Editar datos</CardTitle>
          <CardDescription>
            Deja campos vacíos no aplica aquí: todos los campos son requeridos en
            edición completa.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form
            className="grid gap-4 md:grid-cols-2"
            onSubmit={form.handleSubmit((v) => saveUnidad.mutate(v))}
          >
            <div className="grid gap-2 md:col-span-2">
              <Label>Número económico</Label>
              <Input {...form.register("numero_economico")} />
            </div>
            <div className="grid gap-2">
              <Label>Placas</Label>
              <Input {...form.register("placas")} />
            </div>
            <div className="grid gap-2">
              <Label>Kilometraje actual (solo lectura en API parcial — usa botón)</Label>
              <Input
                type="number"
                disabled
                value={unidad.kilometraje_actual}
                readOnly
              />
            </div>
            <div className="grid gap-2">
              <Label>Marca</Label>
              <Input {...form.register("marca")} />
            </div>
            <div className="grid gap-2">
              <Label>Modelo</Label>
              <Input {...form.register("modelo")} />
            </div>
            <div className="grid gap-2">
              <Label>Año</Label>
              <Input
                type="number"
                {...form.register("anio", { valueAsNumber: true })}
              />
            </div>
            <div className="grid gap-2">
              <Label>Tipo</Label>
              <Input {...form.register("tipo_vehiculo")} />
            </div>
            <div className="grid gap-2 md:col-span-2">
              <Label>Estado</Label>
              <Select
                // react-hook-form watch: RHF + Select controlado
                value={form.watch("estado") ?? "activa"} // eslint-disable-line react-hooks/incompatible-library
                onValueChange={(v) =>
                  form.setValue("estado", v as UnidadForm["estado"])
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="activa">Activa</SelectItem>
                  <SelectItem value="taller">Taller</SelectItem>
                  <SelectItem value="baja">Baja</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="md:col-span-2">
              <Button type="submit" disabled={saveUnidad.isPending}>
                Guardar cambios
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row flex-wrap items-center justify-between gap-4 space-y-0">
          <div>
            <CardTitle>Mantenimientos</CardTitle>
            <CardDescription>
              Historial para la unidad {unidad.placas}.
            </CardDescription>
          </div>
          <Dialog>
            <DialogTrigger render={<Button>Registrar mantenimiento</Button>} />
            <DialogContent className="max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Nuevo mantenimiento</DialogTitle>
              </DialogHeader>
              <form
                className="space-y-3"
                onSubmit={mantForm.handleSubmit((v) => createMant.mutate(v))}
              >
                <div className="grid gap-2">
                  <Label>Tipo</Label>
                  <Input {...mantForm.register("tipo")} />
                </div>
                <div className="grid gap-2">
                  <Label>Fecha (ISO o dd/mm/aaaa)</Label>
                  <Input type="date" {...mantForm.register("fecha_servicio")} />
                </div>
                <div className="grid gap-2 sm:grid-cols-2">
                  <div className="grid gap-2">
                    <Label>Kilometraje</Label>
                    <Input
                      type="number"
                      {...mantForm.register("kilometraje", {
                        valueAsNumber: true,
                      })}
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label>Costo</Label>
                    <Input
                      type="number"
                      step="0.01"
                      {...mantForm.register("costo", { valueAsNumber: true })}
                    />
                  </div>
                </div>
                <div className="grid gap-2">
                  <Label>Proveedor</Label>
                  <Input {...mantForm.register("proveedor")} />
                </div>
                <div className="grid gap-2">
                  <Label>Responsable</Label>
                  <Input {...mantForm.register("responsable")} />
                </div>
                <div className="grid gap-2">
                  <Label>Observaciones</Label>
                  <Textarea {...mantForm.register("observaciones")} />
                </div>
                <DialogFooter>
                  <Button type="submit" disabled={createMant.isPending}>
                    Guardar mantenimiento
                  </Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        </CardHeader>
        <CardContent>
          {mq.isLoading ? (
            <p className="text-muted-foreground">Cargando historial…</p>
          ) : mantenimientos.length === 0 ? (
            <p className="text-muted-foreground">
              Sin mantenimientos registrados.
            </p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Fecha</TableHead>
                  <TableHead>Tipo</TableHead>
                  <TableHead>Km</TableHead>
                  <TableHead>Costo</TableHead>
                  <TableHead className="text-right">Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {mantenimientos.map((m) => (
                  <TableRow key={m.id}>
                    <TableCell>{m.fecha_servicio}</TableCell>
                    <TableCell>{m.tipo}</TableCell>
                    <TableCell>{m.kilometraje}</TableCell>
                    <TableCell>{Number(m.costo).toFixed(2)}</TableCell>
                    <TableCell className="text-right">
                      <AlertDialog>
                        <AlertDialogTrigger
                          render={
                            <Button size="sm" variant="destructive">
                              Eliminar
                            </Button>
                          }
                        />
                        <AlertDialogContent>
                          <AlertDialogHeader>
                            <AlertDialogTitle>
                              ¿Eliminar mantenimiento?
                            </AlertDialogTitle>
                            <AlertDialogDescription>
                              Esta acción no se puede deshacer.
                            </AlertDialogDescription>
                          </AlertDialogHeader>
                          <AlertDialogFooter>
                            <AlertDialogCancel>Cancelar</AlertDialogCancel>
                            <AlertDialogAction
                              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
                              onClick={() => delMant.mutate(m.id)}
                            >
                              Eliminar
                            </AlertDialogAction>
                          </AlertDialogFooter>
                        </AlertDialogContent>
                      </AlertDialog>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
