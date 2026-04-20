"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

import {
  Card,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import * as api from "@/lib/api";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function MantenimientosPage() {
  const q = useQuery({
    queryKey: ["mantenimientos-global"],
    queryFn: () => api.listMantenimientosGlobal(200),
  });

  if (q.isLoading) {
    return (
      <p className="text-muted-foreground">Cargando mantenimientos…</p>
    );
  }
  if (q.isError) {
    return (
      <p className="text-destructive">
        Error al cargar: {(q.error as Error).message}
      </p>
    );
  }

  const rows = q.data ?? [];

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Mantenimientos</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Historial de servicios registrados en toda la flota (más recientes
          primero).
        </p>
      </div>

      <Card className="border-dashed bg-muted/30">
        <CardHeader className="py-4">
          <CardTitle className="text-base">¿Próximos mantenimientos?</CardTitle>
          <CardDescription>
            Aquí aparecen los{" "}
            <strong className="text-foreground">servicios ya realizados</strong>.
            En la{" "}
            <Link href="/" className="font-medium text-primary underline-offset-4 hover:underline">
              página principal
            </Link>{" "}
            puedes ver sugerencias de cuándo conviene el siguiente preventivo
            para los vehículos en operación.
          </CardDescription>
        </CardHeader>
      </Card>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Fecha servicio</TableHead>
              <TableHead>Económico</TableHead>
              <TableHead>Placas</TableHead>
              <TableHead>Tipo</TableHead>
              <TableHead>Km</TableHead>
              <TableHead className="text-right">Costo</TableHead>
              <TableHead className="text-right">Unidad</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.length === 0 ? (
              <TableRow>
                <TableCell
                  colSpan={7}
                  className="text-center text-muted-foreground"
                >
                  No hay mantenimientos registrados.
                </TableCell>
              </TableRow>
            ) : (
              rows.map((m) => (
                <TableRow key={m.id}>
                  <TableCell>{m.fecha_servicio}</TableCell>
                  <TableCell className="font-medium">
                    {m.numero_economico}
                  </TableCell>
                  <TableCell>{m.placas}</TableCell>
                  <TableCell>{m.tipo}</TableCell>
                  <TableCell>
                    {m.kilometraje.toLocaleString("es-MX")}
                  </TableCell>
                  <TableCell className="text-right tabular-nums">
                    ${Number(m.costo).toFixed(2)}
                  </TableCell>
                  <TableCell className="text-right">
                    <Link
                      href={`/unidades/${m.unidad_id}`}
                      className={cn(
                        buttonVariants({ variant: "outline", size: "sm" }),
                      )}
                    >
                      Ver unidad
                    </Link>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
