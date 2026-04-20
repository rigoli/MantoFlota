"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { usePathname } from "next/navigation";
import * as React from "react";

import { buttonVariants } from "@/components/ui/button";
import {
  Card,
  CardContent,
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
import { AUTH_CHANGED_EVENT, clearAuthToken, getAuthToken } from "@/lib/auth";
import type { UsuarioMe } from "@/lib/types";
import { cn } from "@/lib/utils";

function fmtDate(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString("es-MX", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function fmtKm(n: number): string {
  return n.toLocaleString("es-MX");
}

function fmtDateTime(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString("es-MX", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

export function HomeDashboard() {
  const pathname = usePathname();
  const [me, setMe] = React.useState<UsuarioMe | null>(null);
  const [ready, setReady] = React.useState(false);

  const refreshSession = React.useCallback(() => {
    const t = getAuthToken();
    if (!t) {
      queueMicrotask(() => {
        setMe(null);
        setReady(true);
      });
      return;
    }
    api
      .getMe()
      .then((u) => {
        queueMicrotask(() => {
          setMe(u);
          setReady(true);
        });
      })
      .catch(() => {
        clearAuthToken();
        queueMicrotask(() => {
          setMe(null);
          setReady(true);
        });
      });
  }, []);

  React.useEffect(() => {
    refreshSession();
  }, [pathname, refreshSession]);

  React.useEffect(() => {
    const onAuth = () => refreshSession();
    window.addEventListener(AUTH_CHANGED_EVENT, onAuth);
    return () => window.removeEventListener(AUTH_CHANGED_EVENT, onAuth);
  }, [refreshSession]);

  const dashQ = useQuery({
    queryKey: ["dashboard-inicio"],
    queryFn: () => api.getDashboardInicio(),
    enabled: ready && !!me,
  });

  if (!ready) {
    return (
      <div className="flex flex-col gap-8">
        <div className="grid gap-4 md:grid-cols-2">
          <Card className="animate-pulse">
            <CardHeader className="space-y-2">
              <div className="h-6 w-32 rounded bg-muted" />
              <div className="h-10 rounded bg-muted" />
            </CardHeader>
            <CardContent>
              <div className="h-10 w-36 rounded bg-muted" />
            </CardContent>
          </Card>
          <Card className="animate-pulse">
            <CardHeader className="space-y-2">
              <div className="h-6 w-40 rounded bg-muted" />
              <div className="h-10 rounded bg-muted" />
            </CardHeader>
            <CardContent>
              <div className="h-10 w-40 rounded bg-muted" />
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  const ctasUnidadesHref = me ? "/unidades" : "/login?next=/unidades";
  const ctasMantHref = me ? "/mantenimientos" : "/login?next=/mantenimientos";

  return (
    <div className="flex flex-col gap-8">
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Unidades</CardTitle>
            <CardDescription>
              Alta, consulta, edición, kilometraje y estado operativo.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Link
              href={ctasUnidadesHref}
              className={cn(buttonVariants({ variant: "default" }))}
            >
              {me ? "Ir a unidades" : "Iniciar sesión para continuar"}
            </Link>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Mantenimientos</CardTitle>
            <CardDescription>
              Historial global de servicios y seguimiento de preventivos.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Link
              href={ctasMantHref}
              className={cn(buttonVariants({ variant: "secondary" }))}
            >
              {me ? "Ir a mantenimientos" : "Iniciar sesión para continuar"}
            </Link>
          </CardContent>
        </Card>
      </div>

      {me ? (
        <div className="flex flex-col gap-6">
          {dashQ.isLoading ? (
            <p className="text-sm text-muted-foreground">
              Cargando información…
            </p>
          ) : dashQ.isError ? (
            <p className="text-sm text-destructive">
              No se pudo cargar la información: {(dashQ.error as Error).message}
            </p>
          ) : (
            <>
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-lg">
                    Próximos mantenimientos sugeridos
                  </CardTitle>
                  <CardDescription>
                    Fechas y kilómetros orientativos según el último servicio y
                    el uso del vehículo (unidades en operación). Si aún no hay
                    histórico, se toma la fecha de alta y el kilometraje actual.
                  </CardDescription>
                </CardHeader>
                <CardContent className="px-0 pb-2 pt-0">
                  {(dashQ.data?.proximos_mantenimientos.length ?? 0) === 0 ? (
                    <p className="px-6 text-sm text-muted-foreground">
                      No hay vehículos en operación con una sugerencia disponible.
                    </p>
                  ) : (
                    <div className="rounded-md border md:mx-6">
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Económico</TableHead>
                            <TableHead>Placas</TableHead>
                            <TableHead>Vehículo</TableHead>
                            <TableHead>Último servicio</TableHead>
                            <TableHead className="text-right">
                              Km en último servicio
                            </TableHead>
                            <TableHead>Próx. fecha</TableHead>
                            <TableHead className="text-right">Próx. km</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {dashQ.data!.proximos_mantenimientos.map((r) => (
                            <TableRow key={r.unidad_id}>
                              <TableCell>
                                <Link
                                  href={`/unidades/${r.unidad_id}`}
                                  className="font-medium text-primary underline-offset-4 hover:underline"
                                >
                                  {r.numero_economico}
                                </Link>
                              </TableCell>
                              <TableCell>{r.placas}</TableCell>
                              <TableCell>
                                {r.marca} {r.modelo}
                              </TableCell>
                              <TableCell>
                                {fmtDate(r.ultima_fecha_servicio ?? undefined)}
                              </TableCell>
                              <TableCell className="text-right">
                                {r.ultimo_kilometraje_en_servicio != null
                                  ? fmtKm(r.ultimo_kilometraje_en_servicio)
                                  : "—"}
                              </TableCell>
                              <TableCell>
                                {fmtDate(r.proxima_fecha_estimada)}
                              </TableCell>
                              <TableCell className="text-right">
                                {fmtKm(r.proximo_kilometraje_estimado)}
                              </TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </div>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-lg">
                    Por salir de taller
                  </CardTitle>
                  <CardDescription>
                    Vehículos en mantenimiento o reparación; los más recientes
                    aparecen primero.
                  </CardDescription>
                </CardHeader>
                <CardContent className="px-0 pb-2 pt-0">
                  {(dashQ.data?.unidades_en_taller.length ?? 0) === 0 ? (
                    <p className="px-6 text-sm text-muted-foreground">
                      No hay vehículos en taller en este momento.
                    </p>
                  ) : (
                    <div className="rounded-md border md:mx-6">
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Económico</TableHead>
                            <TableHead>Placas</TableHead>
                            <TableHead>Vehículo</TableHead>
                            <TableHead className="text-right">
                              Km actual
                            </TableHead>
                            <TableHead>Actualizado</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {dashQ.data!.unidades_en_taller.map((r) => (
                            <TableRow key={r.unidad_id}>
                              <TableCell>
                                <Link
                                  href={`/unidades/${r.unidad_id}`}
                                  className="font-medium text-primary underline-offset-4 hover:underline"
                                >
                                  {r.numero_economico}
                                </Link>
                              </TableCell>
                              <TableCell>{r.placas}</TableCell>
                              <TableCell>
                                {r.marca} {r.modelo}
                              </TableCell>
                              <TableCell className="text-right">
                                {fmtKm(r.kilometraje_actual)}
                              </TableCell>
                              <TableCell>{fmtDateTime(r.actualizado_en)}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </div>
                  )}
                </CardContent>
              </Card>
            </>
          )}
        </div>
      ) : null}
    </div>
  );
}
