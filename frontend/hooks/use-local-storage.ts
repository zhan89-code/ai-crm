"use client"
import { useState, useEffect } from "react"
export function useLocalStorage<T>(key: string, init: T): [T, (v: T) => void] {
  const [v, setV] = useState<T>(init)
  useEffect(() => { try { const i = window.localStorage.getItem(key); if (i) setV(JSON.parse(i)) } catch {} }, [key])
  const set = (val: T) => { setV(val); try { window.localStorage.setItem(key, JSON.stringify(val)) } catch {} }
  return [v, set]
}
