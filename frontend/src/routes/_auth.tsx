import { createFileRoute, redirect, Outlet } from '@tanstack/react-router'
import { Navbar } from './components/Navbar'

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
            <main className='main_body flex-1 flex flex-col relative min-h-0 w-full overflow-hidden z-1'>
                <Outlet /> 
            </main>
        </div>
    )
}