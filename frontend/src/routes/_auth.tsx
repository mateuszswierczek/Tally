import { createFileRoute, redirect, Outlet } from '@tanstack/react-router'
import { Navbar } from './components/navbar'
import { Sidebar } from './components/Subnavbar'
import { DownloadButton } from './components/DownloadButton'

export const Route = createFileRoute('/_auth')({
    beforeLoad: ({ context }) => {
        if (!context.token) {
            throw redirect({ to: '/' })
        }
    },
    component: AuthLayout
})

function AuthLayout() {
    return (
        <div className='flex flex-col h-screen w-full bg-[#111318] overflow-hidden'>
            <Navbar /> 
            <Sidebar /> 
            <main className='flex-1 flex flex-col relative min-h-0 w-full overflow-hidden'>
                <Outlet /> 
            </main>
            <div className='h-16 shrink-0 border-t border-[#2D3748] bg-[#181c24] flex items-center px-10'>
                <DownloadButton />
            </div>
        </div>
    )
}