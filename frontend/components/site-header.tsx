"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import * as React from "react";

import { ThemeToggle } from "@/components/theme-toggle";
import { Button, buttonVariants } from "@/components/ui/button";
import * as api from "@/lib/api";
import { AUTH_CHANGED_EVENT, clearAuthToken, getAuthToken } from "@/lib/auth";
import type { UsuarioMe } from "@/lib/types";
import { cn } from "@/lib/utils";

export function SiteHeader() {
  const router = useRouter();
  const pathname = usePathname();
  const [me, setMe] = React.useState<UsuarioMe | null>(null);

  const refreshSession = React.useCallback(() => {
    const t = getAuthToken();
    if (!t) {
      queueMicrotask(() => setMe(null));
      return;
    }
    api
      .getMe()
      .then((u) => queueMicrotask(() => setMe(u)))
      .catch(() => {
        clearAuthToken();
        queueMicrotask(() => setMe(null));
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

  function logout() {
    clearAuthToken();
    setMe(null);
    router.replace("/login");
    router.refresh();
  }

  return (
    <header className="border-b bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
        <Link href="/" className="font-semibold tracking-tight">
          MantoFlota
        </Link>
        <nav className="flex flex-wrap items-center gap-2">
          <Link
            href="/"
            className={cn(
              buttonVariants({
                variant: pathname === "/" ? "secondary" : "ghost",
              }),
            )}
          >
            Inicio
          </Link>
          {me ? (
            <>
              <Link
                href="/unidades"
                className={cn(buttonVariants({ variant: "ghost" }))}
              >
                Unidades
              </Link>
              <Link
                href="/mantenimientos"
                className={cn(buttonVariants({ variant: "ghost" }))}
              >
                Mantenimientos
              </Link>
              <span className="hidden text-sm text-muted-foreground sm:inline">
                {me.nombre}{" "}
                <span className="text-xs">({me.rol})</span>
              </span>
              <Button type="button" variant="outline" size="sm" onClick={logout}>
                Salir
              </Button>
            </>
          ) : (
            <Link
              href="/login"
              className={cn(buttonVariants({ variant: "secondary", size: "sm" }))}
            >
              Entrar
            </Link>
          )}
          <ThemeToggle />
        </nav>
      </div>
    </header>
  );
}
