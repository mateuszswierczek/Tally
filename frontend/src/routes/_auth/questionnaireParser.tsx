import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { useEffect } from 'react'
import { DownloadDocButton } from '../components/DownloadDocButton'
import { SurveyQuestion } from '../-schemas'
import { QuestionContainer } from '../components/QuestionContainer'
import z from 'zod'

export const Route = createFileRoute('/_auth/questionnaireParser')({
  component: questionnaireParser,
})

function questionnaireParser() {
    const MapperSchema = z.array(SurveyQuestion);
    type Mapping = z.infer<typeof MapperSchema>;
    const [mapping, setMapping] = useState<Mapping>()
    const [currentQuestionIndex, SetCurrentQuestionIndex] = useState<number | null>(null)
    
    const currentQuestionEdit = currentQuestionIndex !== null && mapping
        ? mapping[currentQuestionIndex]
        : null;

    useEffect(() => {
        const raw =  sessionStorage.getItem("wordData");
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

    function deleteItemFromSetMapping(i:number){
        setMapping(prev => {
            const updated = [...prev!];
            updated.splice(Number(i), 1);
            return updated
        })
    }

   return (
    <>
    <div className='bg-[#111318] flex flex-col w-full h-full overflow-hidden'>
        <div className='w-full flex-1 grid grid-cols-4 pt-4 ml-4 min-h-0'>
            {mapping &&
                <div className='col-span-1 z-2
                rounded-2xl border-2 ml-1 mt-1 w-full h-full overflow-hidden
                p-2 bg-[#181c24] flex flex-col border-[#2D3748]'>
                {mapping && Object.entries(mapping).map(([i, item]) => (
                    <QuestionContainer i={Number(i)}
                    item={item}
                    setCurrentQuestionIndex={SetCurrentQuestionIndex}
                    setMapping={deleteItemFromSetMapping}
                    ></QuestionContainer>
                ))}
                </div>}
            {currentQuestionEdit &&
                <div className='col-span-2 rounded-2xl border-2 ml-5 mt-1 w-full h-full z-2 overflow-hidden
                    p-2 bg-[#181c24] flex flex-col border-[#2D3748]'>
                        <div className='text-white'>
                            <div className='flex flex-col'>
                                <label htmlFor="question">Treść pytania: </label> 
                                <input id={"question"} className="bg-white text-black w-[80%] h-[15%]" type="text" value={currentQuestionEdit.text} onChange={(e) => {
                                    setMapping(prev => {
                                        const updated = [...prev!];
                                        updated[currentQuestionIndex!] = {
                                            ...updated[currentQuestionIndex!],
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
                                        const updated = [...prev!];
                                        updated[currentQuestionIndex!] = {
                                            ...updated[currentQuestionIndex!],
                                            question_type: e.target.value,
                                        };
                                        return updated;
                                    });
                                }}>
                                    <option value={"single"}>Pojedyńczy wybór</option>
                                    <option value={"maq"}>Wielokrotnego wyboru</option>
                                    <option value={"text"}>Tekstowa</option>
                                    <option value={"tabel"}>Tabela</option>
                                    <option value={"numerical"}>Numeryczna</option>
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
                        </div>
                </div>
            }
        </div>
    </div>
    {mapping && 
        <DownloadDocButton mapping={mapping}/>
    }
    </>
); 
}
