import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import {
  Sheet, SheetTrigger, SheetContent, SheetHeader, SheetTitle, SheetDescription, SheetFooter, SheetClose,
} from '@/components/ui/sheet';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';

export default function Storyline() {
  const [campaigns, setCampaigns] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/campaigns')
      .then((res) => res.json())
      .then((data) => setCampaigns(data))
      .catch((err) => console.error('Error fetching campaigns:', err));
  }, []);

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline">Storyline</Button>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Storyline & Campaigns</SheetTitle>
          <SheetDescription>Current storylines and campaigns in progress.</SheetDescription>
        </SheetHeader>
        <ScrollArea className="h-[400px] rounded-md border my-4">
          <div className="p-4">
            {campaigns.map((campaign, idx) => (
              <div key={idx}>
                <h2 className="font-semibold text-lg">{campaign.name}</h2>
                <p>{campaign.description}</p>
                <p className="font-medium">Progress: {campaign.progress}%</p>
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
