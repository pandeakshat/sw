import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import {
  Sheet,
  SheetTrigger,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetFooter,
  SheetClose,
  SheetDescription,
} from '@/components/ui/sheet';

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
          <SheetDescription>Current active effects on your stats</SheetDescription>
        </SheetHeader>
        <div className="py-4">
          {statuses.map((status) => (
            <div key={status.name} className="mb-4 border-b pb-2">
              <h2 className="font-semibold text-lg">{status.name} ({status.grade})</h2>
              <p>{status.description}</p>
              <p className="italic">
                {status['attribute affected']}: {status.value}
              </p>
            </div>
          ))}
        </div>
        <SheetFooter>
          <SheetClose asChild>
            <Button variant="outline">Close</Button>
          </SheetClose>
        </SheetFooter>
      </SheetContent>
    </Sheet>
  );
}
