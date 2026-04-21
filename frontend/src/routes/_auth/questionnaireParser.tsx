import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { useEffect } from 'react'

export const Route = createFileRoute('/_auth/questionnaireParser')({
  component: questionnaireParser,
})

function questionnaireParser() {
    const [mapping, SetMapping] = useState()

    useEffect(() => {
        const raw =  sessionStorage.getItem("excelData");
        if (!raw){
            console.error("No mapping item")
            return
        }
            try {
                SetMapping(JSON.parse(raw))
            }
            catch (e){
            }
    }, [])

    console.log(mapping)

   return (
    <div className='h-full'>
        {mapping && Object.entries(mapping).map(([key, val]) => (
            <div key={key}>
                <p className='text-white'>{key}</p>
            </div>
        ))}
    </div>
); 
}
