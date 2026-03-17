import { createFileRoute } from '@tanstack/react-router'
import { Navbar } from '../components/navbar'
import { Button } from '@/components/ui/button'
import { useState } from 'react'
import './navbar.css'


export const Route = createFileRoute('/_auth/dashboard')({
  component: RouteComponent,
}) 

function RouteComponent() {
  const [isPopUp, setIsPopUp] = useState<boolean>(false);
  
  function handleImportPopUp() {
    setIsPopUp(true ? isPopUp === false : false);
  }

  async function handleSubmitFile(e:React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault()
    const form = new FormData(e.currentTarget);
    const file = form.get("file") as File;

    if (file === null){
      console.log("Brak pliku");
      return
    }

    const req = await fetch("http://127.0.0.1:8000/api/post_excel",{
      method: "POST",
      headers:{
        "Authorization":  `Bearer ${localStorage.getItem('token')}`
      },
      body: form
    })

    if (req.ok){
      console.log(req.json())
    }
    console.error("brak odp.")

  }

  return <>
    <Navbar></Navbar>
    <Button type='button' onClick={handleImportPopUp}>Importuj plik</Button>
    <div className='w-full h-full'>
    {isPopUp &&
      <div className='file-input-popup z-1 w-100 h-25 relative top-1/3 left-38/100 bg-amber-100 border-4 rounded-[16px]'>
        <form className='h-full flex flex-col justify-around items-center' onSubmit={(e) => {handleSubmitFile(e)}}>
          <input id="file" name="file" type='file' className='bg-[#a0adc6] w-5/6 px-4 border-none rounded-2xl' required></input>
          <div className='flex flex-row w-100 justify-evenly'>
            <Button type='submit'>Dalej</Button>
            <Button type='submit' onClick={handleImportPopUp}>Wstecz</Button>
          </div>
        </form>
      </div>
    }
    </div>
  </>
}
