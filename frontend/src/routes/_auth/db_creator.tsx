import { createFileRoute } from '@tanstack/react-router'
import { useSelectionContainer } from '@air/react-drag-to-select'
import { useState } from 'react';

export const Route = createFileRoute('/_auth/db_creator')({
  component: DBCreator,
})

interface MousePos {
    mouse_x: number;
    mouse_y: number;
}

interface Section {
    id: number;
    x: number;
    y: number;
    width: number;
    height: number;
}

function DBCreator() {
    const [sections, setSections] = useState<Section[]>([]);
    const [mousePosStart, setMousePosStart] = useState<MousePos | null>(null);
    
    const { DragSelection } = useSelectionContainer({
        onSelectionStart: (e) => {
            setMousePosStart({
                mouse_x: e.pageX,
                mouse_y: e.pageY,
            });
        },
        onSelectionEnd: (e) => {
            if (!mousePosStart) return;
            
            const endX = e.pageX;
            const endY = e.pageY;
            
            const x = Math.min(mousePosStart.mouse_x, endX);
            const y = Math.min(mousePosStart.mouse_y, endY);
            
            const newSection: Section = {
                id: Date.now(),
                x: x,
                y: y,
                width: Math.abs(mousePosStart.mouse_x - endX), 
                height: Math.abs(mousePosStart.mouse_y - endY), 
            };
            
            setSections(prev => [...prev, newSection]);
        }   
    });

    return (
        <div className='relative z-2 w-full h-screen'>
            <DragSelection/>
            <div className='text-white'>Element</div>
            
            {sections.map(section => (
                <div 
                    key={section.id}
                    className='bg-black absolute border border-white'
                    style={{ 
                        left: `${section.x}px`,
                        top: `${section.y - 100}px`,
                        width: `${section.width}px`, 
                        height: `${section.height}px` 
                    }}
                />
            ))}
        </div>
    );
}