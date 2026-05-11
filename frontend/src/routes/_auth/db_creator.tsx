import { createFileRoute } from '@tanstack/react-router'
import { Box, boxesIntersect, useSelectionContainer } from '@air/react-drag-to-select'
import { useState, useRef, useEffect } from 'react';
import { useMapping } from '@/context/MappingContext';
import { date } from 'zod';

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
    const refElement = useRef<Box[]>([]);
    
    const selectableItemsIndices = useRef<number[]>([]);
    
    const elementsContainerRef = useRef<HTMLDivElement | null>(null);
    const {mapping, setMapping} = useMapping();   
    const [drawableQuestions, setDrawableQuestions] = useState<[]>([]);
    
    const [selectedMappingItems, setSelectedMappingItems] = useState<any[]>([]);

    const updateSelectableItems = () => {
        if (elementsContainerRef.current) {
            selectableItems.current = [];
            selectableItemsIndices.current = [];

            const items = elementsContainerRef.current.querySelectorAll('[data-selectable="true"]')
            items.forEach((item) => {
                const index = parseInt(item.getAttribute('data-mapping-index') || '-1');
                
                const { left, top, width, height} = item.getBoundingClientRect();
                selectableItems.current.push({
                    left: left + window.scrollX,
                    top: top + window.scrollY,
                    width,
                    height,
                });
                
                selectableItemsIndices.current.push(index);
            });
        }
    };

    const { DragSelection } = useSelectionContainer({
        shouldStartSelecting: (target) => {
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
            updateSelectableItems();
            
            const scrollAwareBox: Box = {
                ...box,
                top: box.top + window.scrollY,
                left: box.left + window.scrollX
            };

            setSelectionBox(scrollAwareBox);
            const indexesToSelect: number[] = [];
            
            selectableItems.current.forEach((item, index) => {
                if (boxesIntersect(scrollAwareBox, item)) {
                    indexesToSelect.push(index);
                }
            });

            setSelectedIndexes(indexesToSelect);
            
            const selectedItems = indexesToSelect.map(idx => {
                const mappingIndex = selectableItemsIndices.current[idx];
                return drawableQuestions[mappingIndex];
            }).filter(Boolean);
            
            setSelectedMappingItems(selectedItems);
        },
        selectionProps: {
            style:{
                zIndex: 3,
            }
        },

        onSelectionStart: (e) => {
            setMousePosStart({
                mouse_x: e.pageX,
                mouse_y: e.pageY,
            });
        },
        //TODO: Poprawić to, bo nie działa ze zmianą strony 
        onSelectionEnd: (e) => {
            const clamp = (num, min, max) => Math.min(Math.max(num, min), max);
            
            if (!mousePosStart) return;
            
            const ref = elementsContainerRef.current?.getBoundingClientRect();
            if (!ref) return;
            
            const refLeft = ref.left + window.scrollX;
            const refTop = ref.top + window.scrollY;
            const refRight = refLeft + ref.width;
            const refBottom = refTop + ref.height;
            
            const startX = clamp(mousePosStart.mouse_x, refLeft, refRight);
            const startY = clamp(mousePosStart.mouse_y, refTop, refBottom);
            const endX = clamp(e.pageX, refLeft, refRight);
            const endY = clamp(e.pageY, refTop, refBottom);
            
            const rawX = Math.min(startX, endX);
            const rawY = Math.min(startY, endY);
            const width = Math.abs(startX - endX);
            const height = Math.abs(startY - endY);

            const x = clamp(rawX, refLeft, refRight - width);
            const y = clamp(rawY, refTop, refBottom - height);
            
            const newSection: Section = {
                id: Date.now(),
                x: x,
                y: y - 80,
                width: width,
                height: height,
            };
            
            setSections(prev => [...prev, newSection]);
}
    });

    useEffect(() => {
        updateSelectableItems();
    }, [drawableQuestions]);

    return (
        <div className='bg-[#111318] flex flex-col w-full h-full overflow-hidden'>
            <DragSelection/>
            <div className='w-full z-2 flex-1 mb-10 grid grid-cols-4 pt-4 ml-4 min-h-0'>
                <div className='col-span-1 
                    rounded-2xl ml-1 w-full h-full overflow-hidden
                    p-2 bg-[#181c24] flex flex-col border border-[#2D3748]' data-disableselect="true">
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
                        }}>
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
                            type='submit'>
                            Dalej
                        </button>
                    </form>
                </div>
                <div className='col-span-2 h-full ml-5 bg-[#181c24] text-white w-full border border-[#2D3748] rounded-lg relative' ref={elementsContainerRef}>
                    {drawableQuestions &&
                    drawableQuestions.map((value, index) => (
                        <div 
                            className='w-25 h-15 ml-10 mt-10 bg-[#181c24] z-10 border-[#E8821A] border-2 rounded-[16px] relative'
                            key={index}
                            data-selectable="true"
                            data-mapping-index={index}>
                            {value.question}
                        </div>
                    ))}
                    {sections.map(section => (
                        <div 
                            key={section.id}
                            className='bg-[#1113185b] rounded-2xl absolute border border-white pointer-events-none'
                            style={{ 
                                left: `${section.x - 400}px`,
                                top: `${section.y}px`,
                                width: `${section.width}px`, 
                                height: `${section.height}px` 
                            }}/>
                    ))}
                </div>
            </div>
        </div>
    );
}