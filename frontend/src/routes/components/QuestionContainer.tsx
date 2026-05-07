import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/components/QuestionContainer')({
  component: QuestionContainer,
})

function QuestionContainer(i:number, item:Object, SetCurrentQuestionIndex:CallableFunction, setMapping:CallableFunction) {
  return <div className='h-fit min-h-15 w-full mb-5 z-1 pr-4 pl-4 flex flex-col items-center '>
            <div className='border-[0.5px]
                border-[#E8821A] rounded-[5px] w-full bg-[#E8821A]
                flex justify-end items-center pr-0.5 z-0'>
                <button key={i} className='text-white p-1.5 h-[95%] w-[95%] bg-[#181c24]' onClick={() => SetCurrentQuestionIndex(Number(i))}>
                    <div className='flex flex-row w-full justify-between'>
                        <p>{item.index}</p>
                        <p className='overflow-clip'>{item.question_type}</p>
                    </div>
                    <p className='overflow-hidden'>{item.text}</p>
                </button>
                <button onClick={() => {
                    setMapping(prev => {
                        const updated = [...prev!];
                        updated.splice(Number(i), 1);
                        return updated
                    })
                }}>X</button>
            </div>
        </div>
}
