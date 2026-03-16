import { createFileRoute, redirect, Outlet } from '@tanstack/react-router'

export const Route = createFileRoute('/_auth')({
    beforeLoad: ({context}) =>{
        if (!context.token){
            throw redirect({to: '/'})
        }
    },
    component: () => <Outlet/>
})