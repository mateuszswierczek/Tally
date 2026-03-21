import { createFileRoute } from '@tanstack/react-router'
import { Navbar } from '../components/navbar'
import './navbar.css'

export const Route = createFileRoute('/_auth/projects')({
  component: RouteComponent,
})

function RouteComponent() {
    return <>
        <Navbar></Navbar>
    </>
}
