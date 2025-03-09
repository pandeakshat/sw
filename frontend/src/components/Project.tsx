import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import {
  Sheet,
  SheetTrigger,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
  SheetFooter,
  SheetClose,
} from '@/components/ui/sheet';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Separator } from '@/components/ui/separator';

export default function Project() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/projects')
      .then((res) => res.json())
      .then((data) => setProjects(data))
      .catch((err) => console.error('Error fetching projects:', err));
  }, []);

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline">Projects</Button>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Projects Overview</SheetTitle>
          <SheetDescription>All current projects and their progress.</SheetDescription>
        </SheetHeader>
        <ScrollArea className="h-[800px] rounded-md border my-4">
          <div className="p-4">
            {projects.map((project, idx) => (
              <div key={idx}>
                <h2 className="font-semibold text-lg">{project.name}</h2>
                <p>{project.description}</p>
                <p className="font-medium">Progress: {project.progress}%</p>
                {project.link && (
                  <a href={project.link} target="_blank" className="text-blue-500 underline">
                    View Project →
                  </a>
                )}
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
