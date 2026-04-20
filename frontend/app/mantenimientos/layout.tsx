"use client";

import { usePathname, useRouter } from "next/navigation";
import * as React from "react";

import { getAuthToken } from "@/lib/auth";

export default function MantenimientosLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [ready, setReady] = React.useState(false);

  React.useEffect(() => {
    if (!getAuthToken()) {
      router.replace(`/login?next=${encodeURIComponent(pathname)}`);
      return;
    }
    queueMicrotask(() => setReady(true));
  }, [router, pathname]);

  if (!ready) {
    return (
      <div className="text-sm text-muted-foreground" aria-live="polite">
        Comprobando sesión…
      </div>
    );
  }

  return children;
}
