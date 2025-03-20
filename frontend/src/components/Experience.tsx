"use client"

import { useState, useEffect } from 'react';
import { Progress } from '@/components/ui/progress';

export default function ExperienceBar() {
  const [progress, setProgress] = useState(0);
  const [level, setLevel] = useState(1);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/experience')
      .then(res => res.json())
      .then(data => {
        setProgress(data.progress_percentage);
        setLevel(data.current_level);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="w-full">
      <div className="text-center mb-2">Level: {level}</div>
      <Progress value={progress} className="w-full" />
      <div className="mt-1 text-center">{progress.toFixed(2)}%</div>
    </div>
  );
}
