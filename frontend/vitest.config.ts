import path from "node:path";
import { fileURLToPath } from "node:url";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

const root = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./vitest.setup.tsx"],
    css: true,
    exclude: [
      "**/node_modules/**",
      "**/e2e/**",
      "**/.next/**",
    ],
  },
  resolve: {
    alias: {
      "@": path.resolve(root, "."),
    },
  },
});
