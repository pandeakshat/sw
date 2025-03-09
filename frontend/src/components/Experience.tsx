"use client"

import * as React from "react"

import { Progress } from "@/components/ui/progress"

export function ExperienceBar() {
  const [progress, setProgress] = React.useState(15)

  React.useEffect(() => {
    const timer = setTimeout(() => setProgress(1), 500)
    return () => clearTimeout(timer)
  }, [])

  return <Progress value={progress} className="w" />
}
