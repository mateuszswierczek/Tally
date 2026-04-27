import { createFileRoute, redirect, Outlet } from '@tanstack/react-router'
import { Navbar } from './components/navbar'
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
            <main className='flex-1 flex flex-col relative min-h-0 w-full overflow-hidden'>
                <Outlet /> 
            </main>
        </div>
    )
}