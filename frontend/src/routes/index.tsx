// TODO (security):
// [ ] KRYTYCZNE: przenieść token z localStorage do httpOnly cookie (podatność na XSS)
// [ ] zablokować przycisk submit podczas ładowania (zapobiec wielokrotnym requestom)
// [ ] dodać autocomplete="username" i autocomplete="current-password" na inputach
// [ ] naprawić toggle widoczności hasła 

import { useState } from 'react'
import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import './login.css'

export const Route = createFileRoute('/')({
  component: HomeComponent,
})

function HomeComponent() {
  const navigate = useNavigate();
  const [error, setError] = useState<boolean | null>(null);

  async function handleSubmit(e:React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const form_data =new URLSearchParams();
    form_data.append("username", form.get("login") as string);
    form_data.append("password", form.get("password") as string);

    const res = await fetch("http://127.0.0.1:8000/api/auth_user", {
      method:'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body:form_data.toString()})
    
    if (res.ok){
      const { access_token } = await res.json();
      localStorage.setItem('token', access_token);
      navigate({to: "/dashboard"});
    }
    setError(true)
  }

  return (
  <div className='flex flex-row h-screen overflow-hidden'>
    <div className='left gap-2.5 relative font-["Fraunces"] px-10 py-12 border-r border-[#2a3040] overflow-hidden flex flex-col w-120 h-105 bg-[#181c24] min-h-screen'>
      <div className='login-heading z-1 relative flex-row mb-20'>
        <p className='text-4xl font-thin mb-2 text-white'>Witaj z <span className='italic text-[#E8821A]'>powrotem</span></p>
        <p className='text-[15px] text-[#525c72] font-["DM Sans"] relative'>Zaloguj się do platformy</p>
      </div>
      <div className='z-1 relative'>
        <form className='form' onSubmit={handleSubmit}>
          <div className='form-div flex flex-col'>
            {error && <div className='login-error w-full h-10 mb-2 border rounded-[8xp] flex justify-center border-solid items-center border-[#c03a2b67] bg-[#f6867a22]'>
              <p className='text-red-300 text-xl font-["DM_Mono"]'>Błędne hasło lub login.</p>
            </div>}
            <label className='text-[13px] mb-1 text-[#525c72] font-["DM_Mono"] relative' htmlFor="login">Login</label>
            <Input required className='input h-10.75 text-[14px] mb-3 bg-[#1e2330] font-["DM_Sans"] outline-hidden text-[#eceef2] border rounded-[8px] border-[#323a4e]'
              id="login" name="login" type='text' placeholder='Wpisz swój login'></Input>
            <label className='text-[13px] mb-1 text-[#525c72] font-["DM_Mono"] relative' htmlFor="password">Hasło</label>
            <div className='relative mb-5'>
              <Input required className='input h-10.75 text-[14px] bg-[#1e2330] font-["DM_Sans"] outline-hidden text-[#eceef2] border rounded-[8px] border-[#323a4e] w-full pr-10' placeholder='*******' id="password" name="password" type='password'></Input>
              <div className='absolute right-3 top-1/2 -translate-y-1/2 text-[#525c72] text-[16px] cursor-pointer'>👁</div>
            </div>
          </div>
          <Button className='btn-login w-full h-10.75 mt-1 relative rounded-[8px] overflow-hidden border-none px-3 text-[14px] font-extrabold cursor-pointer font-["DM_Sans"] bg-[#E8821A] text-white' id="submit_btn" type='submit'>
           Zaloguj się →
          </Button>
        </form>
      </div>
      <div className='z-1 relative mt-6'>
        <img src="https://media1.tenor.com/m/-kZOB16tELEAAAAC/this-is-fine-fire.gif" alt="This is fine" className='w-full rounded-[8px] opacity-60' />
      </div>
      <div className='mt-auto pt-4 z-1 relative'>
        <p className='text-[12px] font-["DM_Mono"] text-[#8c909a]'>Tally <span className='ml-1'>v0.1.0</span></p>
      </div>
    </div>
    <div className='divider'></div>
    <div className='right relative w-screen h-screen flex flex-col items-center justify-center bg-[#111318]'>
      <div className='z-1 w-120 h-60 overflow-hidden'>
        <img src="https://i.ibb.co/bR6JZ3Kh/1773547344326-removebg-preview.png" className='w-full h-full object-contain scale-250'></img>
      </div>
      <div className='z-1 text-center'>
        <p className='text-[28px] font-["Fraunces"] font-thin text-white mb-2'>Analiza danych</p>
        <p className='text-[16px] font-["DM_Sans"] text-[#525c72] max-w-xs mx-auto'>Importuj, przetwarzaj i analizuj dane.</p>
      </div>
    </div>
  </div>
  )
}
