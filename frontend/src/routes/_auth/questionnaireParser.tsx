import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { useEffect } from 'react'
import { DownloadDocButton } from '../components/DownloadDocButton'

export const Route = createFileRoute('/_auth/questionnaireParser')({
  component: questionnaireParser,
})

function questionnaireParser() {
    const [mapping, setMapping] = useState()
    const [currentQuestionIndex, SetCurrentQuestionIndex] = useState<number>()

    
    const currentQuestionEdit = currentQuestionIndex !== null && mapping
        ? mapping[currentQuestionIndex]
        : null;

    useEffect(() => {
        const raw =  sessionStorage.getItem("excelData");
        if (!raw){
            console.error("No mapping item")
            return
        }
            try {
                setMapping(JSON.parse(raw))
            }
            catch (e){
            }
    }, [])

   return (
    <>
    <div className='bg-[#111318] flex flex-col w-full h-full overflow-hidden'>
        <div className='w-full flex-1 grid grid-cols-4 pt-4 ml-4 min-h-0'>
            <div className='col-span-1 
            rounded-2xl border-2 ml-1 mt-1 w-full h-full overflow-hidden
            p-2 bg-[#181c24] flex flex-col border-[#2D3748]'>
            {mapping && Object.entries(mapping).map(([i, item]) => (
                <div className='h-fit min-h-15 w-full mb-5 z-1 pr-4 pl-4 flex flex-col items-center '>
                    <div className='border-[0.5px]
                        border-[#E8821A] rounded-[5px] w-full bg-[#E8821A]
                        flex justify-end items-center pr-0.5 z-0'>
                        <button key={i} className='text-white p-1.5 h-[95%] w-[95%] bg-[#181c24]' onClick={() => SetCurrentQuestionIndex(Number(i))}>
                            <div className='flex flex-row w-full justify-between'>
                                <p>{item.index}</p>
                                <p className='overflow-clip'>{item.quesion_type}</p>
                            </div>
                            <p className='overflow-hidden'>{item.text}</p>
                        </button>
                    </div>
                </div>
            ))}
            </div>
            {currentQuestionEdit &&
                <div className='col-span-2 rounded-2xl border-2 ml-5 mt-1 w-full h-full overflow-hidden
                    p-2 bg-[#181c24] flex flex-col border-[#2D3748]'>
                        <div className='text-white'>
                            <div className='flex flex-col'>
                                <label htmlFor="question">Treść pytania: </label> 
                                <input id={"question"} className="bg-white text-black w-[80%] h-[15%]" type="text" value={currentQuestionEdit.text} onChange={(e) => {
                                    setMapping(prev => {
                                        const updated = [...prev];
                                        updated[currentQuestionIndex] = {
                                            ...updated[currentQuestionIndex],
                                            text: e.target.value,
                                        };
                                        return updated;
                                    });
                                }}
                                /> 
                            </div>
                            <div>
                                <label htmlFor="type">Typ pytania: </label> 
                                <select id="type" value={currentQuestionEdit.question_type} onChange={(e) => {
                                    console.log(mapping)
                                    setMapping(prev => {
                                        const updated = [...prev];
                                        updated[currentQuestionIndex] = {
                                            ...updated[currentQuestionIndex],
                                            question_type: e.target.value,
                                        };
                                        return updated;
                                    });
                                }}>
                                    <option value={"Pojedyńczy wybór"}>Pojedyńczy wybór</option>
                                    <option value={"Wielokrotnego wyboru"}>Wielokrotnego wyboru</option>
                                    <option value={"Tekstowa"}>Tekstowa</option>
                                    <option value={"Tabela"}>Tabela</option>
                                    <option value={"Numeryczna"}>Numeryczna</option>
                                </select>
                            </div>
                            <div className='flex flex-row'>
                               <div className='w-[50%]'>
                                    <p>Kafeteria</p>
                                    {Object.entries(currentQuestionEdit.cafeteria ?? {}).map((cafe, ind) => (
                                        <div className='mb-2' key={ind}>
                                            <input className='bg-white text-black' type="text" value={cafe[1]["item"]}/>
                                        </div>
                                    ))}
                                </div> 
                                <div className='w-[50%]'>
                                    <p>Subpytania</p>
                                    {Object.entries(currentQuestionEdit.columns ?? {}).map((cafe, ind) => (
                                        <div className='mb-2' key={ind}>
                                            <input  className='bg-white text-black' type="text" value={cafe[1]["item"]}/>
                                        </div>
                                    ))}
                                </div> 
                            </div>
                            {/*TODO: Dodać zmianę typu question_type na backendzie na key enum*/}
                            {/*TODO: Dodać input na typie pytań, iterowanie po kafeterii i subpytaniach, push na backend*/}
                        </div>
                </div>
            }
        </div>
    </div>
    <DownloadDocButton mapping={mapping}/>
    </>
); 
}
