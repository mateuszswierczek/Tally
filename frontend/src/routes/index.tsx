import * as React from 'react'
import { createFileRoute } from '@tanstack/react-router'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

export const Route = createFileRoute('/')({
  component: HomeComponent,
})

function HomeComponent() {
  return (
    <div className='left relative border-r border-[#2a3040] items-center justify-around flex flex-col w-1/2 bg-[#181c24] min-h-screen'>
      <div className='z-1 w-1/2 h-1/2'>
        <img src="https://raw.githubusercontent.com/Openfield-survey/img-hosting/refs/heads/main/logo-op.png" alt="Logo"/>
      </div>
      <div className='z-1 flex-row'>
        <p>Witaj z <p></p>powrotem</p>
        <h1>Zaloguj się do platformy</h1>
      </div>
      <div className='z-1'>
        <form>
          <div className='flex flex-col'>
          <label htmlFor="login">Login</label>
          <Input id="login" name="login" type='text'></Input>
          <label htmlFor="password">Hasło</label>
          <Input id="password" name="password" type='text'></Input>
          </div>
        <Button id="submit_btn" type='submit'>Zaloguj się</Button>
        </form>
      </div>
    </div>
  )
}
