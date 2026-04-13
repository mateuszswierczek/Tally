import { createFileRoute } from '@tanstack/react-router'
import { useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Link } from '@tanstack/react-router'
import '../_auth/navbar.css'

export const Route = createFileRoute('/components/navbar')({
  component: Navbar,
})

export function Navbar() {
  const [activeIndex, setActiveIndex] = useState<number | null>(null)
  const [isPopUp, setIsPopUp] = useState<boolean>(false);
  const navigate = useNavigate();

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
      const data_json = await req.json()
      const excel_data = data_json["mapping"]
      sessionStorage.setItem("excelData", JSON.stringify(excel_data));
      navigate({to:"/recoder"})
    }

  }
  
  return <div className='flex flex-row'>
    <nav className='w-full flex flex-row justify-around h-15 bg-[#181c24]'>
      <div className='w-40 h-30 px-2 py-2 mr-20'>
        <img src="https://raw.githubusercontent.com/Openfield-survey/img-hosting/refs/heads/main/logo-op.png" alt='Logo'></img>
      </div>
      <div className='flex flex-row justify-around items-center h-full w-125 z-1'>
      {[
      {nav_label:"Dashboard", to:"/dashboard"}, 
      {nav_label:"Projekty", to:"/projects"},
      {nav_label:"Recoder", to:"/recoder"}].map((arr, i) => (
        <Link key={i} to={arr.to} className={`nav-option ${activeIndex === i ? "active" : ""} h-full w-30 flex justify-center`} onClick={() => {setActiveIndex(i)}}>
            <span className='text-[#8f96a8] h-full w-fit flex items-center select-none'>{arr.nav_label}</span>
        </Link>
      ))}
      </div>
      <Button className='w-40 self-center bg-[#E8821A]' type='button' onClick={handleImportPopUp}>Importuj plik</Button>
      {isPopUp &&
        //TODO: Zmienić design tego diva
        <div className='file-input-popup z-1 w-100 h-25 absolute top-75 right-200 bg-amber-100 border-4 rounded-[16px]'>
          <form className='h-full flex flex-col justify-around items-center' onSubmit={(e) => {handleSubmitFile(e)}}>
            <input id="file" name="file" type='file' className='bg-[#a0adc6] w-5/6 px-4 border-none rounded-2xl' required></input>
            <div className='flex flex-row w-100 justify-evenly'>
              <Button type='submit'>Dalej</Button>
              <Button type='submit' onClick={handleImportPopUp}>Wstecz</Button>
            </div>
          </form>
        </div>
      }
    </nav>
    <div className='divider'></div>
  </div>
}

