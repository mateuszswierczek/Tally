import ReactDOM from 'react-dom/client'
import { RouterProvider, createRouter } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'
import { getToken } from './auth'
import { MappingProvider } from './context/MappingContext'
import './index.css' 

// Set up a Router instance
const router = createRouter({
  routeTree,
  defaultPreload: 'intent',
  context: {token: getToken},
})

// Register things for typesafety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
  interface RouterContext{
    token: string | null
  }
}

const rootElement = document.getElementById('app')!

if (!rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement)
  root.render(
    <MappingProvider>
      <RouterProvider router={router} />
    </MappingProvider>
  )
}
