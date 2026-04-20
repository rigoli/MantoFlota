import { UnidadClient } from "./unidad-client";

export default async function UnidadPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const num = Number(id);
  if (!Number.isFinite(num)) {
    return <p className="text-destructive">ID inválido</p>;
  }
  return <UnidadClient id={num} />;
}
