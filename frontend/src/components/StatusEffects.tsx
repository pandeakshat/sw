import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import {
  Sheet, SheetTrigger, SheetContent, SheetHeader, SheetTitle, SheetDescription, SheetFooter, SheetClose,
} from '@/components/ui/sheet';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';

export default function StatusEffects() {
  const [statuses, setStatuses] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/status-effects')
      .then((res) => res.json())
      .then((data) => setStatuses(data))
      .catch((err) => console.error('Error fetching status effects:', err));
  }, []);

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline">Status Effects</Button>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Status Effects</SheetTitle>
          <SheetDescription>Active status effects influencing your attributes.</SheetDescription>
        </SheetHeader>
        <ScrollArea className="h-[400px] rounded-md border my-4">
          <div className="p-4">
            {statuses.map((status, idx) => (
              <div key={idx}>
                <h2 className="font-semibold text-lg">{status.name} ({status.grade})</h2>
                <p>{status.description}</p>
                <p className="italic">
                  {status['attribute affected']}: {status.value}
                </p>
                <Separator className="my-3" />
              </div>
            ))}
          </div>
        </ScrollArea>
        <SheetFooter>
          <SheetClose asChild>
            <Button variant="outline">Close</Button>
          </SheetClose>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
