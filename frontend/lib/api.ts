/**
 * Cliente HTTP JSON para MantoFlota API.
 * Usa ``NEXT_PUBLIC_API_URL`` (default http://localhost:8000).
 */

import { getAuthToken } from "@/lib/auth";
import type {
  DashboardInicio,
  Mantenimiento,
  MantenimientoListItem,
  Unidad,
  UsuarioMe,
} from "@/lib/types";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") || "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function parseError(res: Response): Promise<string> {
  try {
    const j = (await res.json()) as { detail?: unknown };
    if (typeof j.detail === "string") return j.detail;
    if (Array.isArray(j.detail)) return JSON.stringify(j.detail);
    if (j.detail) return JSON.stringify(j.detail);
  } catch {
    /* ignore */
  }
  return res.statusText || `HTTP ${res.status}`;
}

export async function fetchJson<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const token = getAuthToken();
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(init?.headers || {}),
    },
    cache: "no-store",
  });
  if (!res.ok) {
    throw new ApiError(await parseError(res), res.status);
  }
  if (res.status === 204) {
    return undefined as T;
  }
  return res.json() as Promise<T>;
}

/** --- Auth --- */

export async function login(
  email: string,
  password: string,
): Promise<{ access_token: string; token_type: string }> {
  const res = await fetch(`${API_BASE}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
    cache: "no-store",
  });
  if (!res.ok) {
    throw new ApiError(await parseError(res), res.status);
  }
  return res.json() as Promise<{ access_token: string; token_type: string }>;
}

export function getMe(): Promise<UsuarioMe> {
  return fetchJson<UsuarioMe>("/api/v1/auth/me");
}

/** --- Panel inicio --- */

export function getDashboardInicio(): Promise<DashboardInicio> {
  return fetchJson<DashboardInicio>("/api/v1/dashboard/inicio");
}

/** --- Unidades --- */

export function listUnidades(): Promise<Unidad[]> {
  return fetchJson<Unidad[]>("/api/v1/unidades");
}

export function getUnidad(id: number): Promise<Unidad> {
  return fetchJson<Unidad>(`/api/v1/unidades/${id}`);
}

export function createUnidad(body: Omit<Unidad, "id" | "creado_en" | "actualizado_en">): Promise<Unidad> {
  return fetchJson<Unidad>("/api/v1/unidades", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function updateUnidad(
  id: number,
  body: Partial<Omit<Unidad, "id" | "creado_en" | "actualizado_en">>,
): Promise<Unidad> {
  return fetchJson<Unidad>(`/api/v1/unidades/${id}`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

export function deleteUnidad(id: number): Promise<void> {
  return fetchJson<void>(`/api/v1/unidades/${id}`, { method: "DELETE" });
}

export function patchKilometraje(
  id: number,
  kilometraje_actual: number,
): Promise<Unidad> {
  return fetchJson<Unidad>(`/api/v1/unidades/${id}/kilometraje`, {
    method: "PATCH",
    body: JSON.stringify({ kilometraje_actual }),
  });
}

/** --- Mantenimientos --- */

export function listMantenimientosGlobal(limit = 150): Promise<
  MantenimientoListItem[]
> {
  const q = new URLSearchParams({ limit: String(limit) });
  return fetchJson<MantenimientoListItem[]>(
    `/api/v1/mantenimientos?${q}`,
  );
}

export function listMantenimientosPorUnidad(
  unidadId: number,
): Promise<Mantenimiento[]> {
  return fetchJson<Mantenimiento[]>(
    `/api/v1/unidades/${unidadId}/mantenimientos`,
  );
}

export function createMantenimiento(
  unidadId: number,
  body: Omit<Mantenimiento, "id" | "unidad_id" | "creado_en" | "actualizado_en">,
): Promise<Mantenimiento> {
  return fetchJson<Mantenimiento>(
    `/api/v1/unidades/${unidadId}/mantenimientos`,
    {
      method: "POST",
      body: JSON.stringify(body),
    },
  );
}

export function updateMantenimiento(
  id: number,
  body: Partial<
    Omit<Mantenimiento, "id" | "unidad_id" | "creado_en" | "actualizado_en">
  >,
): Promise<Mantenimiento> {
  return fetchJson<Mantenimiento>(`/api/v1/mantenimientos/${id}`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

export function deleteMantenimiento(id: number): Promise<void> {
  return fetchJson<void>(`/api/v1/mantenimientos/${id}`, {
    method: "DELETE",
  });
}
