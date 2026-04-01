import { createFileRoute } from '@tanstack/react-router'
<<<<<<< HEAD
import { Button } from '@/components/ui/button'
import { Navbar } from '../components/navbar'
import { useState } from 'react'
import { useEffect } from 'react'
import { MappingSchema, CafeteriaSchema } from '../_schemas'
import { z } from 'zod';
=======
import { Navbar } from '../components/navbar'
import { useState } from 'react'
import { useEffect } from 'react'
import { MappingSchema } from '../-schemas'
import { z } from 'zod';
import { DragDropProvider } from '@dnd-kit/react'
import { useSortable, isSortableOperation } from '@dnd-kit/react/sortable'
import { DragEndEvent } from '@dnd-kit/dom'
>>>>>>> b6ead16 (Working on frontend parsing)
import './navbar.css'

export const Route = createFileRoute('/_auth/recoder')({
  component: RouteComponent,
})
const Schema = MappingSchema;
const MapperSchema = z.array(Schema);
type Mapping = z.infer<typeof MapperSchema>;
type Question = z.infer<typeof Schema>;

<<<<<<< HEAD
function RouteComponent() {
    const [mapping, setMapping] = useState<Mapping | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [fuzzyQuestionMatching, setQuestionFuzzyMatching] = useState<string | null>(null) 
    const [currentQuestionEdit, setCurrentQuestionEdit] = useState<Question>()

=======

function SortableItem({ id, index }: { id: string; index: number }) {
    const { ref } = useSortable({ id, index });
    return (
        <div ref={ref} className='w-full h-fit text-white cursor-grab border mt-2 mb-2 text-center'>
            {id}
        </div>
    );
}

function RouteComponent() {
    const [mapping, setMapping] = useState<Mapping | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [fuzzyQuestionMatching, setQuestionFuzzyMatching] = useState<string | null>(null)
    const [currentQuestionEdit, setCurrentQuestionEdit] = useState<Question>()

    function handleDragEnd(event: Parameters<DragEndEvent>[0], questionIndex: number) {
        const { operation } = event;
        if (!isSortableOperation(operation)) return;
        const { source, target } = operation;
        if (!source || !target || source.index === target.index) return;
        setMapping(prev => {
            if (!prev) return prev;
            const next = [...prev];
            const subqs = [...(next[questionIndex].subquestions ?? [])];
            const [moved] = subqs.splice(source.index, 1);
            subqs.splice(target.index, 0, moved);
            next[questionIndex] = { ...next[questionIndex], subquestions: subqs };
            return next;
        });
    }

>>>>>>> b6ead16 (Working on frontend parsing)
    useEffect(() => {
        const stored = sessionStorage.getItem('excelData');

        if (!stored) {
            console.log("error: brak danych");
            return;
        }

        const result = MapperSchema.safeParse(JSON.parse(stored));

        if (result.success) {
            setMapping(result.data);
        } else {
            setError(result.error.toString());
            console.error(result.error.issues);
        }
    }, []);

    if (error) return <p style={{ color: "red" }}>{error}</p>;
    if (!mapping) return <p>Ładowanie...</p>;

    const DownloadButton = () => {
        const handleDatabaseDownload = async () => {
            console.log(JSON.stringify(mapping))
            
            const req = await fetch("http://127.0.0.1:8000/api/post_mapping", {
                method:"POST",
                headers:{
                    "Content-Type": "application/json",
                    "Authorization" : `Bearer ${localStorage.getItem("token")}`
                },
                body: JSON.stringify(mapping),
            })
            
            if (!req.ok){
                console.error("Błąd w bazie")
                return
            }
            const file = await req.blob()
            const download_url = URL.createObjectURL(file);
            const link = document.createElement('a')

            link.href = download_url
            link.download = 'Baza.zip'
            link.click()
            URL.revokeObjectURL(download_url)
        }
        return <button onClick={handleDatabaseDownload}>Pobierz bazę</button>
    }
        
    return (
        <div className='bg-[#111318] h-screen w-screen flex flex-col'>
            <Navbar />
            <div className='w-full h-[80%] grid grid-cols-4 grid-rows-1 pt-4'>
                <div className='col-span-1 border-[#111318]
                rounded-2xl border-2 ml-1 mt-1 w-full h-full
                p-2 bg-[#181c24] flex flex-col'>
                    <input type='text' className='w-[90%] mr-2 bg-white mt-4 mb-4'
                    onChange={(e) => {setQuestionFuzzyMatching(e.currentTarget.value)}}></input>
                    <div className='flex-1 min-h-0 w-full overflow-y-auto'>
                        {mapping && Object.values(mapping).map((item, i) => {
<<<<<<< HEAD
=======
                            const isSubquestion = true ? item.subquestions !== null : false
>>>>>>> b6ead16 (Working on frontend parsing)
                            const isQuestionVisible = fuzzyQuestionMatching == null || 
                                item.question?.toLowerCase().includes(fuzzyQuestionMatching.toLowerCase())
                            return(
                                <>
                                    {isQuestionVisible &&
<<<<<<< HEAD
                                        <div className='h-18 w-full mb-5 z-1 pr-4 pl-4'>
                                            <div className='h-[calc(100%+10px)] border-[0.5px]
=======
                                        <div className='h-fit min-h-15 w-full mb-5 z-1 pr-4 pl-4 flex flex-col'>
                                            <div className='border-[0.5px]
>>>>>>> b6ead16 (Working on frontend parsing)
                                                border-[#E8821A] rounded-[5px] w-full bg-[#E8821A] 
                                                flex justify-end items-center pr-0.5 z-0'>
                                                    <button key={i} className='text-white p-1.5 h-[95%] w-[95%] bg-[#181c24]' onClick={(_) => {setCurrentQuestionEdit(item)}}>
                                                        <div className='flex flex-row w-full justify-between'>
                                                            <p>{item.index}</p>
                                                            <p className='overflow-clip'>{item.type}</p>
                                                        </div>
                                                        <p className='overflow-hidden'>{item.question}</p>
                                                    </button>
                                            </div>
<<<<<<< HEAD
=======
                                            {
                                                isSubquestion &&
                                                <DragDropProvider onDragEnd={(event) => handleDragEnd(event, i)}>
                                                    {item.subquestions!.map((subquestion, index) => (
                                                        <SortableItem key={subquestion.question} id={subquestion.question} index={index} />
                                                    ))}
                                                </DragDropProvider>
                                            }
>>>>>>> b6ead16 (Working on frontend parsing)
                                        </div>
                                    }
                                </>
                            )})}
                    </div>
                </div>
                <div className='grid grid-cols-1 text-white col-span-2 bg-[#181c24] mt-1 ml-4 w-full h-full'>
                    {currentQuestionEdit && 
                    <div>
                        <div className='h-[10%] pt-2 pl-2'>
                            <p>{currentQuestionEdit.question}</p>
                            <div className='flex flex-row justify-between w-[80%] '>
                                <p>Typ: {currentQuestionEdit.type}</p>
                                <p>Unikatowe wartości: {currentQuestionEdit.unique_count}</p>
                                <p>Braki danych: {currentQuestionEdit.missing_count}</p>
                                <p>N: {currentQuestionEdit.total_count}</p>
                            </div>
                        </div>
                        <div className='grid grid-cols-6 h-fit w-full pl-2'>
                              <div className='contents font-bold'>
                                <span>ID</span>
                                <span>Kategoria</span>
                                <span>Częstości</span>
                                <span>Dystrybucja</span>
                                <span>Index</span>
                                <span>Missing type</span>
                            </div>
<<<<<<< HEAD
                            {Object.entries(currentQuestionEdit.cafeteria_dump).map(([key, cafe], i) => (
=======
                            {Object.entries(currentQuestionEdit.cafeteria_dump ?? {}).map(([key, cafe], i) => (
>>>>>>> b6ead16 (Working on frontend parsing)
                                <div key={i} className='contents'>
                                    <span>{key}</span>
                                    <span>{cafe.value}</span>
                                    <span>{cafe.n}</span>
                                    <span>{cafe.distribution}</span>
                                    <input type='text' value={cafe.index} onChange={(e) => {
                                        const newCafeteria = [...(currentQuestionEdit!.cafeteria_dump ?? [])];
                                        newCafeteria[i] = { ...newCafeteria[i], index: Number(e.currentTarget.value) };
                                        const updatedQuestion = { ...currentQuestionEdit!, cafeteria_dump: newCafeteria };
                                        setCurrentQuestionEdit(updatedQuestion);
                                        setMapping(mapping!.map(q => q === currentQuestionEdit ? updatedQuestion : q));
                                }}></input>
                                    <span>{cafe.missing_type}</span>
                                </div>
                            ))}
                        </div> 
                    </div>
                    }
               </div>
                <div className='w-full'>
                    <p>Test</p>
                </div>
            </div>
            <div className='w-[98%] h-full flex flex-row justify-between border rounded-2xl items-center mt-5 mb-5 ml-4 mr-4 text-white bg-[#181c24]'>
                <div className='pl-10'>
                    <span>Zmienne</span>

                </div>
                <div className='pr-10'>
                    <DownloadButton></DownloadButton>
                </div>
            </div>
        </div>
    );
}
