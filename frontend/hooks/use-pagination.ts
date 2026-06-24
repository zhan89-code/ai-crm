"use client"
import { useState, useCallback } from "react"
export function usePagination(initPage = 1, initSize = 20) {
  const [page, setPage] = useState(initPage)
  const [size, setSize] = useState(initSize)
  const reset = useCallback(() => setPage(1), [])
  return { page, setPage, pageSize: size, setPageSize: setSize, reset }
}
