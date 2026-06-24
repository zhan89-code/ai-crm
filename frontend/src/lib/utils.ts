import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
}

export function tierColor(tier: string): string {
  const colors: Record<string, string> = {
    hot: "bg-red-100 text-red-800",
    warm: "bg-orange-100 text-orange-800",
    cold: "bg-blue-100 text-blue-800",
  };
  return colors[tier] || "bg-gray-100 text-gray-800";
}
