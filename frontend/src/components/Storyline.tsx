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
          <SheetTitle>Campaign & Storyline</SheetTitle>
          <SheetDescription>Ongoing storylines and campaigns</SheetDescription>
        </SheetHeader>
        <div className="py-4 space-y-4">
          {campaigns.map((campaign) => (
            <div key={campaign.name} className="border p-3 rounded-lg shadow-sm">
              <h2 className="font-semibold text-lg">{campaign.name}</h2>
              <p>{campaign.description}</p>
              <p className="font-medium">Progress: {campaign.progress}%</p>
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
