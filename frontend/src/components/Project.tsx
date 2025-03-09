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
          <SheetTitle>Your Projects</SheetTitle>
          <SheetDescription>
            Current running projects and their progress.
          </SheetDescription>
        </SheetHeader>
        <div className="py-4 space-y-4">
          {projects.map((project) => (
            <div key={project.name} className="border p-2 rounded-lg shadow-sm">
              <h2 className="font-semibold text-lg">{project.name}</h2>
              <p>{project.description}</p>
              <p className="font-medium">Progress: {project.progress}%</p>
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
