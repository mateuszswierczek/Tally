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
    const [fuzzyMatching, setFuzzyMatching] = useState<string | null>(null) 

    useEffect(() => {
        const stored = sessionStorage.getItem('excelData');

        if (!stored) {
            console.log("error: brak danych");
            return;
        }

        const result = MapperSchema.safeParse(JSON.parse(stored)); // ← JSON.parse!

        if (result.success) {
            setMapping(result.data);
        } else {
            setError(result.error.toString());
            console.error(result.error.issues); // pokaże dokładnie co się nie zgadza
        }
    }, []);

    if (error) return <p style={{ color: "red" }}>{error}</p>;
    if (!mapping) return <p>Ładowanie...</p>;


        
    return (
        <>
            <Navbar />
                <div className='recoder-sidbar border-[#111318]
                rounded-2xl border-2 ml-1 mt-1 flex flex-col
                p-2 overflow-scroll w-[30%] h-full bg-[#181c24] items-center'>
                    <input type='text' className='mb-2 w-[90%] mr-2 bg-white' 
                    onChange={(e) => {setFuzzyMatching(e.currentTarget.value)}}></input>
                    {mapping && Object.values(mapping).map((item, i) => {
                        const isVisible = fuzzyMatching == null || 
                            item.question?.toLowerCase().includes(fuzzyMatching.toLowerCase())
                         
                        return(
                            //TODO: Naprawić
                            <div className='h-full w-full mb-5 z-1'>
                                <div className='h-[calc(100%+10px)] border-[0.5px]
                                    border-[#E8821A] rounded-[5px] w-full bg-[#E8821A] 
                                    flex justify-end items-center pr-0.5 z-0'>
                                        <div key={i} className='text-white p-1.5 h-[95%] w-[95%] bg-[#181c24]'>
                                            <div className='flex flex-row w-full justify-between'>
                                                <p>{item.index}</p>
                                                <p className='overflow-clip'>{item.type}</p>
                                            </div>
                                            <p className='overflow-hidden'>{item.question}</p>
                                        </div>
                                </div>
                            </div>
                    )})}
                </div>
        </>
    );
}
