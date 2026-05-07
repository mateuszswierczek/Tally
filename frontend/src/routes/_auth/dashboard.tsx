import { createFileRoute } from '@tanstack/react-router'
import { Navbar } from '../components/Navbar'
import { Sidebar } from '../components/Subnavbar'

export const Route = createFileRoute('/_auth/dashboard')({
  component: RouteComponent,
}) 

function RouteComponent() {

  return <>
  </>
}
