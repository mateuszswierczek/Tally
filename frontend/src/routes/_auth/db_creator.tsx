import { createFileRoute } from '@tanstack/react-router'
import { Box, boxesIntersect, useSelectionContainer } from '@air/react-drag-to-select'
import { useState, useRef } from 'react';
import { useMapping } from '@/context/MappingContext';

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
    const [selectionBox, setSelectionBox] = useState<Box>();
    const [selectedIndexes, setSelectedIndexes] = useState<number[]>([]);
    const selectableItems = useRef<Box[]>([]);
    const elementsContainerRef = useRef<HTMLDivElement | null>(null);
    const {mapping, setMapping} = useMapping();   
    const [drawableQuestions, setDrawableQuestions] = useState<[]>([]);

    const { DragSelection } = useSelectionContainer({
        shouldStartSelecting: (target) => {
            /**
             * In this example, we're preventing users from selecting in elements
             * that have a data-disableselect attribute on them or one of their parents
             */
            if (target instanceof HTMLElement) {
            let el = target;
            while (el.parentElement && !el.dataset.disableselect) {
                el = el.parentElement;
            }
            return el.dataset.disableselect !== "true";
            }
            return false;
        },
        onSelectionChange: (box) => {
            const scrollAwareBox: Box = {
                ...box,
                top: box.top + window.scrollY,
                left: box.left + window.scrollX
            };
            console.log(scrollAwareBox)

            setSelectionBox(scrollAwareBox);
            const indexesToSelect: number[] = [];
            selectableItems.current.forEach((item, index) => {
                if (boxesIntersect(scrollAwareBox, item)) {
                indexesToSelect.push(index);
                }
            });

            setSelectedIndexes(indexesToSelect);
        },
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
        <div className='bg-[#111318] flex flex-col w-full h-full overflow-hidden'>
            <div className='w-full z-2 flex-1 mb-10 grid grid-cols-4 pt-4 ml-4 min-h-0'>
                <div className='col-span-1 
                    rounded-2xl ml-1 w-full h-full overflow-hidden
                    p-2 bg-[#181c24] flex flex-col border border-[#2D3748]' data-disableselect>
                    <form 
                        className='text-white h-full flex flex-col'
                        onSubmit={(e) => {
                            e.preventDefault();
                            const select = e.target.elements.question;
                            const selectedOptions = Array.from(select.selectedOptions);
                            const selectedQuestions = selectedOptions.map(option => {
                                const index = parseInt(option.getAttribute('data-index'));
                                return mapping[index];
                            });
                            setDrawableQuestions(selectedQuestions);
                            console.log(selectedQuestions);
                        }}
                    >
                        <select className='h-[90%] w-full' name='question' id='question' multiple>
                            {mapping && 
                                mapping.map((value, index) => (
                                    <option key={index} data-index={index}>
                                        {value.question}
                                    </option>
                                ))
                            }
                        </select>
                        <button 
                            className='w-25 h-15 bg-[#181c24] border-[#E8821A] border-2 rounded-[16px]' 
                            type='submit'
                        >
                            Dalej
                        </button>
                    </form>
                </div>
                <div className='col-span-2 h-full ml-5 bg-[#181c24] text-white w-full border border-[#2D3748] rounded-lg'>
                    <DragSelection/>
                    {drawableQuestions &&
                    drawableQuestions.map((value, index) => (
                        <div className='w-25 h-15 ml-10 mt-10 bg-[#181c24] border-[#E8821A] border-2 rounded-[16px]' key={index}>{value.question}</div>
                    ))}
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
            </div>
        </div>
    );
}