"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { toast } from "sonner";

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
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import * as api from "@/lib/api";
import { cn } from "@/lib/utils";

export default function UnidadesPage() {
  const qc = useQueryClient();
  const q = useQuery({
    queryKey: ["unidades"],
    queryFn: api.listUnidades,
  });

  const del = useMutation({
    mutationFn: api.deleteUnidad,
    onSuccess: async () => {
      toast.success("Unidad eliminada");
      await qc.invalidateQueries({ queryKey: ["unidades"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  if (q.isLoading) {
    return <p className="text-muted-foreground">Cargando unidades…</p>;
  }
  if (q.isError) {
    return (
      <p className="text-destructive">
        Error al cargar: {(q.error as Error).message}. ¿Está el API en{" "}
        <code className="rounded bg-muted px-1">NEXT_PUBLIC_API_URL</code>?
      </p>
    );
  }

  const rows = q.data ?? [];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Unidades</h1>
          <p className="text-sm text-muted-foreground">
            {rows.length === 0
              ? "No hay unidades registradas."
              : `${rows.length} unidad(es) en el sistema.`}
          </p>
        </div>
        <Link
          href="/unidades/nueva"
          className={cn(buttonVariants({ variant: "default" }))}
        >
          Nueva unidad
        </Link>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>#</TableHead>
              <TableHead>Económico</TableHead>
              <TableHead>Placas</TableHead>
              <TableHead>Marca / Modelo</TableHead>
              <TableHead>Km</TableHead>
              <TableHead>Estado</TableHead>
              <TableHead className="text-right">Acciones</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map((u) => (
              <TableRow key={u.id}>
                <TableCell>{u.id}</TableCell>
                <TableCell className="font-medium">{u.numero_economico}</TableCell>
                <TableCell>{u.placas}</TableCell>
                <TableCell>
                  {u.marca} {u.modelo}
                </TableCell>
                <TableCell>{u.kilometraje_actual.toLocaleString("es-MX")}</TableCell>
                <TableCell>
                  <Badge variant="secondary">{u.estado}</Badge>
                </TableCell>
                <TableCell className="space-x-2 text-right">
                  <Link
                    href={`/unidades/${u.id}`}
                    className={cn(
                      buttonVariants({ variant: "outline", size: "sm" }),
                    )}
                  >
                    Ver
                  </Link>
                  <AlertDialog>
                    <AlertDialogTrigger
                      render={
                        <Button variant="destructive" size="sm">
                          Eliminar
                        </Button>
                      }
                    />
                    <AlertDialogContent>
                      <AlertDialogHeader>
                        <AlertDialogTitle>¿Eliminar unidad?</AlertDialogTitle>
                        <AlertDialogDescription>
                          Se eliminarán también los mantenimientos asociados.
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>Cancelar</AlertDialogCancel>
                        <AlertDialogAction
                          onClick={() => del.mutate(u.id)}
                          className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
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
      </div>
    </div>
  );
}
