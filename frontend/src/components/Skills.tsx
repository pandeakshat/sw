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

export default function Skills() {
  const [skills, setSkills] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/skills')
      .then((res) => res.json())
      .then((data) => setSkills(data))
      .catch((err) => console.error('Error fetching skills:', err));
  }, []);

  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="outline">Skills</Button>
      </SheetTrigger>
      <SheetContent>
        <SheetHeader>
          <SheetTitle>Your Skills & Talents</SheetTitle>
          <SheetDescription>Overview of your skills and talents</SheetDescription>
        </SheetHeader>
        <div className="py-4">
          {skills.map((skill) => (
            <div key={skill.name} className="mb-4 border-b pb-2">
              <h2 className="font-semibold text-lg">{skill.name} ({skill.grade})</h2>
              <p>{skill.description}</p>
              <p className="italic">
                {skill['attribute affected']}: {skill.value}
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
