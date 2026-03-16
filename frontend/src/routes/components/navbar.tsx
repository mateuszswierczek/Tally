import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { Link } from '@tanstack/react-router'
import '../_auth/navbar.css'

export const Route = createFileRoute('/components/navbar')({
  component: Navbar,
})

export function Navbar() {
  const [activeIndex, setActiveIndex] = useState<number | null>(null)
  
  return <div className='flex flex-row'>
    <nav className='w-full flex flex-row h-15 bg-[#181c24]'>
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
    </nav>
    <div className='divider'></div>
  </div>
}

