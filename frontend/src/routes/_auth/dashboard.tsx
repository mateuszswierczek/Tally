import { createFileRoute } from '@tanstack/react-router'
import { Navbar } from '../components/navbar'


export const Route = createFileRoute('/_auth/dashboard')({
  component: RouteComponent,
}) 

function RouteComponent() {

  return <>
    <Navbar></Navbar>
  </>
}
