import { HomeDashboard } from "@/components/home-dashboard";

export default function Home() {
  return (
    <div className="flex flex-1 flex-col gap-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">MantoFlota</h1>
        <p className="mt-2 max-w-2xl text-muted-foreground">
          Centraliza tus unidades, el historial de servicios y el seguimiento del
          mantenimiento preventivo en un solo lugar.
        </p>
      </div>
      <HomeDashboard />
    </div>
  );
}
