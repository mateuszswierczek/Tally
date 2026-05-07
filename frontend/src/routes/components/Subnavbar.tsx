import { createFileRoute } from '@tanstack/react-router'
import { Link } from '@tanstack/react-router'
import { useState } from 'react'
import '../_auth/navbar.css'

export const Route = createFileRoute('/components/Subnavbar')({
  component: Sidebar,
})

export function Sidebar() {
  const [activeIndex, setActiveIndex] = useState<number | null>(null)
    return <div className='flex flex-row w-screen h-fit justify-around bg-[#2c313c]'>
    {[
      {nav_label:"Rekodowanie", to:"/recoder"}, 
      {nav_label:"Krzyżówki", to:"/crosstables"},
      {nav_label:"Kreator", to:"/db_creator"},
      {nav_label:"Regresja liniowa", to:"/linear_reg"}].map((arr, i) => (
        <Link key={i} to={arr.to} className={`nav-option ${activeIndex === i ? "active" : ""} h-full w-30 flex justify-center`} onClick={() => {setActiveIndex(i)}}>
            <span className='text-white text-[14px] h-full w-fit flex items-center select-none'>{arr.nav_label}</span>
        </Link>
      ))}
      </div>
}
