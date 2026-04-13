
import { createFileRoute } from '@tanstack/react-router'
import { Navbar } from '../components/navbar'
import { useState } from 'react'
import { useEffect } from 'react'
import { MappingSchema } from '../-schemas'
import { z } from 'zod';
import { DragDropProvider } from '@dnd-kit/react'
import { useSortable, isSortableOperation } from '@dnd-kit/react/sortable'
import { DragEndEvent } from '@dnd-kit/dom'
import './navbar.css'
 
export const Route = createFileRoute('/_auth/recoder')({
  component: RouteComponent,
})
const Schema = MappingSchema;
const MapperSchema = z.array(Schema);
type Mapping = z.infer<typeof MapperSchema>;
type Question = z.infer<typeof Schema>;
 
 
function SortableItem({ id, index }: { id: string; index: number }) {
    const { ref } = useSortable({ id, index });
    return (
        <div ref={ref} className='w-[80%] h-fit text-white cursor-grab border mt-2 mb-2 text-center'>
            {id}
        </div>
    );
}
 
function RouteComponent() {
    const [mapping, setMapping] = useState<Mapping | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [fuzzyQuestionMatching, setQuestionFuzzyMatching] = useState<string | null>(null)
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState<number | null>(null);
 
    const currentQuestionEdit = currentQuestionIndex !== null && mapping
        ? mapping[currentQuestionIndex]
        : null;
 
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

    function getQuestionType(type:string | null){
        console.log(type)
        if (type === "continuous") {
            return "Ciągła"
        }
        else if (type === "nominal"){
            return "Nominalna"
        }
        else if (type === "ordinal"){
            return "Porządkowa"
        }
        else if (type === "text"){
            return "Tekst"
        }
        else {
            return "Inne"
        }
    }
 
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
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                },
                body: JSON.stringify(mapping),
            })
 
            if (!req.ok) {
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
            <div className='w-full h-[80%] grid grid-cols-4 grid-rows-1 pt-4 ml-4'>
                <div className='col-span-1 
                rounded-2xl border-2 ml-1 mt-1 w-full h-full
                p-2 bg-[#181c24] flex flex-col border-[#2D3748]'>
                    <input type='text' placeholder=' Wyszukaj zmiennej...' className='w-[90%] bg-[#181c24] text-white border border-[#2D3748] rounded-lg mr-2 mt-4 mb-4 ml-4'
                        onChange={(e) => { setQuestionFuzzyMatching(e.currentTarget.value) }}></input>
                    <div className='flex-1 min-h-0 w-full overflow-y-auto'>
                        {mapping && Object.values(mapping).map((item, i) => {
                            const isSubquestion = item.subquestions !== null
                            const isQuestionVisible = fuzzyQuestionMatching == null ||
                                item.question?.toLowerCase().includes(fuzzyQuestionMatching.toLowerCase())
                            return (
                                <>
                                    {isQuestionVisible &&
                                        <div className='h-fit min-h-15 w-full mb-5 z-1 pr-4 pl-4 flex flex-col items-center'>
                                            <div className='border-[0.5px]
                                                border-[#E8821A] rounded-[5px] w-full bg-[#E8821A]
                                                flex justify-end items-center pr-0.5 z-0'>
                                                <button key={i} className='text-white p-1.5 h-[95%] w-[95%] bg-[#181c24]' onClick={() => setCurrentQuestionIndex(i)}>
                                                    <div className='flex flex-row w-full justify-between'>
                                                        <p>{item.index}</p>
                                                        <p className='overflow-clip'>{getQuestionType(item.type)}</p>
                                                    </div>
                                                    <p className='overflow-hidden'>{item.question}</p>
                                                </button>
                                            </div>
                                            {
                                                isSubquestion &&
                                                <DragDropProvider onDragEnd={(event) => handleDragEnd(event, i)}>
                                                    {item.subquestions!.map((subquestion, index) => (
                                                        <SortableItem key={subquestion.question} id={subquestion.question} index={index} />
                                                    ))}
                                                </DragDropProvider>
                                            }
                                        </div>
                                    }
                                </>
                            )
                        })}
                    </div>
                </div>
                <div className='grid grid-cols-1 text-white col-span-2 mt-1 ml-4 w-full h-full'>
                    {currentQuestionEdit &&
                        <div>
                            {/* TODO: Zmiana tego na słownik */}
                            <div className='h-[10%] pt-2 pl-2 bg-[#181c24] border border-[#2D3748] mb-5 rounded-lg'>
                                <p className='text-xl'>{currentQuestionEdit.question}</p>
                                <div className='flex flex-row justify-around w-[90%]'>
                                    <span className='flex flex-row text-[18px]'>
                                        <p className='text-[#4B5563]'>Typ:</p> 
                                        <p>{getQuestionType(currentQuestionEdit.type)}</p>
                                    </span>
                                    <span className='flex flex-row text-[18px]'>
                                        <p className='text-[#4B5563]'>Unikatowe wartości:</p> 
                                        <p>{currentQuestionEdit.unique_count}</p>
                                    </span>
                                    <span className='flex flex-row text-[18px]'>
                                        <p className='text-[#4B5563]'>Braki danych:</p> 
                                        <p>{currentQuestionEdit.missing_count}</p>
                                    </span>
                                    <span className='flex flex-row text-[18px]'>
                                        <p className='text-[#4B5563]'>N:</p> 
                                        <p>{currentQuestionEdit.total_count}</p>
                                    </span>
                                </div>
                            </div>
                            <div className='grid grid-cols-6 h-fit bg-[#181c24] w-full border border-[#2D3748] rounded-lg'>
                                {/* TODO:Zmiana na słownik */}
                                <div className='contents font-bold'>
                                    <span className='bg-[#2D3748] h-15 flex items-center justify-center mb-5 rounded-tl-lg'>ID</span>
                                    <span className='bg-[#2D3748] h-15 flex items-center justify-center'>Kategoria</span>
                                    <span className='bg-[#2D3748] h-15 flex items-center justify-center'>Częstości</span>
                                    <span className='bg-[#2D3748] h-15 flex items-center justify-center'>Dystrybucja</span>
                                    <span className='bg-[#2D3748] h-15 flex items-center justify-center'>Index</span>
                                    <span className='bg-[#2D3748] h-15 flex items-center justify-center rounded-r-lg'>Brak danych</span>
                                </div>
                                {Object.entries(currentQuestionEdit.cafeteria_dump ?? {}).map(([key, cafe], i) => (
                                    <div key={i} className='contents'>
                                        <span className='flex items-center justify-center mb-5'>{key}</span>
                                        <span className='flex items-center justify-center mb-5'>{cafe.value}</span>
                                        <span className='flex items-center justify-center mb-5'>{cafe.n}</span>
                                        <span className='flex items-center justify-center mb-5'>{cafe.distribution}</span>
                                        <input className='index-input flex items-center justify-center mb-5 border' type='text' value={cafe.index} onChange={(e) => {
                                            const newCafeteria = [...(currentQuestionEdit.cafeteria_dump ?? [])];
                                            newCafeteria[i] = { ...newCafeteria[i], index: Number(e.currentTarget.value) };
                                            setMapping(prev => prev!.map((q, idx) =>
                                                idx === currentQuestionIndex ? { ...q, cafeteria_dump: newCafeteria } : q
                                            ));
                                        }} />
                                        <span>{cafe.missing_type}</span>
                                    </div>
                                ))}
                                <div>
                                    <label htmlFor="is_maq">Wielokrotny wybór?</label>
                                    <input
                                        id="is_maq"
                                        type="checkbox"
                                        name="is_maq"
                                        checked={!!currentQuestionEdit.is_maq}
                                        onChange={() => {
                                            setMapping(prev => prev!.map((q, idx) =>
                                                idx === currentQuestionIndex ? { ...q, is_maq: !q.is_maq } : q
                                            ));
                                        }}
                                    />
                                </div>
                            </div>
                        </div>
                    }
                </div>
                <div className='col-span-1 ml-8 mr-8 h-full bg-[#181c24] border border-[#2D3748] rounded-2xl'>
                </div>
            </div>
            <div className='w-[98%] h-full flex flex-row justify-between border border-[#2D3748] rounded-2xl items-center mt-5 mb-5 ml-4 mr-4 text-white bg-[#181c24]'>
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
