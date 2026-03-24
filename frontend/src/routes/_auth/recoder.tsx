import { createFileRoute } from '@tanstack/react-router'
import { Navbar } from '../components/navbar'
import { useState } from 'react'
import { useEffect } from 'react'
import { MappingSchema } from '../_schemas'
import { z } from 'zod';
import './navbar.css'

export const Route = createFileRoute('/_auth/recoder')({
  component: RouteComponent,
})
const MapperSchema = z.array(MappingSchema);
type Mapping = z.infer<typeof MapperSchema>;


function RouteComponent() {
    const [mapping, setMapping] = useState<Mapping | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [fuzzyQuestionMatching, setQuestionFuzzyMatching] = useState<string | null>(null) 
    const [currentQuestionEdit, setCurrentQuestionEdit] = useState<Object | null>(null)

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
        
    return (
        <>
            <Navbar />
            <div className='grid grid-cols-4'>
                <div className='recoder-sidbar col-span-1 border-[#111318]
                rounded-2xl border-2 ml-1 mt-1 flex flex-col
                p-2 overflow-scroll h-full bg-[#181c24] items-center'>
                    <input type='text' className='mb-2 w-[90%] mr-2 bg-white' 
                    onChange={(e) => {setQuestionFuzzyMatching(e.currentTarget.value)}}></input>
                    {mapping && Object.values(mapping).map((item, i) => {
                        const isQuestionVisible = fuzzyQuestionMatching == null || 
                            item.question?.toLowerCase().includes(fuzzyQuestionMatching.toLowerCase())
                        return(
                            <>
                                {isQuestionVisible &&
                                    <div className='h-18 w-full mb-5 z-1'>
                                        <div className='h-[calc(100%+10px)] border-[0.5px]
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
                                    </div>
                                }
                            </>
                        )})}
                </div>
                <div className='grid grid-cols-1 text-white col-span-2 bg-[#181c24] mt-1 ml-4'>
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
                            {Object.entries(currentQuestionEdit.cafeteria_dump).map(([key, cafe], i) => (
                                <div key={i} className='contents'>
                                    <span>{key}</span>
                                    <span>{cafe.value}</span>
                                    <span>{cafe.n}</span>
                                    <span>{cafe.distribution}</span>
                                    <input type='text' value={cafe.index}></input>
                                    <span>{cafe.missing_type}</span>
                                </div>
                            ))}
                        </div> 
                    </div>
                    }
               </div>
            </div>
        </>
    );
}
