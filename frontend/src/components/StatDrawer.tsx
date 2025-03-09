import { Button } from '@/components/ui/button';
import {
  Drawer,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
  DrawerClose,
} from '@/components/ui/drawer';

interface Stat {
  name: string;
  value: number;
  breakdown: Record<string, number | string>;
}

interface StatDrawerProps {
  statName: string;
  statData: Stat;
}

export function StatDrawer({ statName, statData }: StatDrawerProps) {
  console.log(`${statName} data:`, statData);
  if (!statData || statData.breakdown.error) {
    return (
      <div class="text-red-500">
        {statName} -- Error: {statData?.breakdown.error || "No data"}
      </div>
    );
  }

  return (
    <Drawer>
      <DrawerTrigger>
        <Button variant="outline">
          {statName} -- {statData.value}
        </Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle><h1 class="text-center">{statName}</h1></DrawerTitle>
          <DrawerDescription><h1 class="text-center">Stat Breakdown</h1></DrawerDescription>
        </DrawerHeader>
        <div class="text-center p-4">
          {Object.entries(statData.breakdown).map(([metric, score]) => (
            <div key={metric}>
              {metric} -- {typeof score === 'number' ? score.toFixed(3) : score}
            </div>
          ))}
        </div>
        <DrawerFooter>
          <DrawerClose>
            <Button variant="outline">Close</Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
}