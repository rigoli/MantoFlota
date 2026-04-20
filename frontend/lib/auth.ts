/** Token Bearer en ``localStorage`` (solo cliente). */

const STORAGE_KEY = "mantoflota_access_token";

/** Evento disparado al cambiar token (login / salir); escuchan header e inicio. */
export const AUTH_CHANGED_EVENT = "mantoflota-auth-changed";

function emitAuthChanged(): void {
  if (typeof window === "undefined") return;
  window.dispatchEvent(new CustomEvent(AUTH_CHANGED_EVENT));
}

export function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(STORAGE_KEY);
}

export function setAuthToken(token: string): void {
  localStorage.setItem(STORAGE_KEY, token);
  emitAuthChanged();
}

export function clearAuthToken(): void {
  localStorage.removeItem(STORAGE_KEY);
  emitAuthChanged();
}
