import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { SiteHeader } from "@/components/site-header";

const STORAGE_KEY = "mantoflota_access_token";

describe("SiteHeader", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL) => {
        const url =
          typeof input === "string"
            ? input
            : input instanceof Request
              ? input.url
              : String(input);
        if (url.includes("/api/v1/auth/me")) {
          return {
            ok: true,
            status: 200,
            json: async () => ({
              id: 1,
              email: "demo@test.com",
              nombre: "Demo",
              rol: "administrador",
            }),
          } as Response;
        }
        return {
          ok: false,
          status: 404,
          json: async () => ({}),
        } as Response;
      }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("muestra marca y enlaces Unidades / Mantenimientos con sesión", async () => {
    localStorage.setItem(STORAGE_KEY, "token-demo");
    render(<SiteHeader />);

    await waitFor(() => {
      expect(screen.getByRole("link", { name: "Unidades" })).toHaveAttribute(
        "href",
        "/unidades",
      );
    });
    expect(screen.getByRole("link", { name: "Mantenimientos" })).toHaveAttribute(
      "href",
      "/mantenimientos",
    );
    expect(screen.queryByRole("link", { name: "Nueva unidad" })).toBeNull();
    expect(screen.getByText("MantoFlota")).toBeInTheDocument();
  });
});
