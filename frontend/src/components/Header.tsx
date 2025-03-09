import { CalendarIcon } from "lucide-react"

import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card"

export function Header() {
  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <Button variant="link"><h1 className="mb-6 text-5xl">Akshat Pande</h1>
        </Button>
      </HoverCardTrigger>
      <HoverCardContent className="w-80">
        <div className="flex justify-between space-x-4">
          <Avatar>
            <AvatarImage src="./avatar.png" />
            <AvatarFallback>AP</AvatarFallback>
          </Avatar>
          <div className="space-y-1">
            <h4 className="text-sm font-semibold">Level 1</h4>
            <p className="text-sm">
              <strong>Race - </strong>  Evolutionary High Human <br />
              <strong>Class - </strong> Chaotic Developer <br />
              <strong>Quest - </strong> Essence Restructure

            </p>
            <div className="flex items-center pt-2">
              <CalendarIcon className="mr-2 h-4 w-4 opacity-70" />{" "}
              <span className="text-xs text-muted-foreground">
                04-01-1996
              </span>
            </div>
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
}
