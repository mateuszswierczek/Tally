import { useMapping } from '@/context/MappingContext'; 
import { useNavigate } from '@tanstack/react-router';
import { Link } from '@tanstack/react-router';
import { Sidebar } from './Subnavbar';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

export function Navbar() {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const [isPopUp, setIsPopUp] = useState<boolean>(false);
  const navigate = useNavigate();
  const { setMapping } = useMapping();
  //TODO: Pzenieść to do zmiennych środowiskowych
  const isExcel = check([0x50, 0x4B, 0x03, 0x04, 0x14, 0x00, 0x06, 0x00])
  const isWord = check([0x50, 0x4B, 0x03, 0x04, 0x14, 0x00, 0x08, 0x08])

  function readBuffer(file:File, start=0, end=8) : Promise<ArrayBuffer>{
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () =>{
        resolve(reader.result as ArrayBuffer)
      };
      reader.onerror = reject;
      reader.readAsArrayBuffer(file.slice(start,end))
    })
  }

  function check(headers:number[]) {
  return (buffers:Uint8Array, options = { offset: 0 }) =>
    headers.every(
      (header, index) => header === buffers[options.offset + index]
    );
}

  async function handleSubmitFile(e: React.SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const file = form.get("file") as File;
    const buffer: ArrayBuffer = await readBuffer(file, 0, 8)
    const u_int = new Uint8Array(buffer)

    if (!file) {
      console.log("Brak pliku");
      return;
    }

    const fetch_addres = isExcel(u_int) 
      ? "http://127.0.0.1:8000/api/post_excel" 
      : isWord(u_int) ? "http://127.0.0.1:8000/api/post_questionnaire" 
      : (() => {
        alert("Błędne rozszerzenie pliku.")
        throw new Error("Błędny plik.")})();

    const req = await fetch(fetch_addres, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem('token')}`
      },
      body: form
    });

    if (req.ok) {
      const data_json = await req.json();
      const mapping_data = data_json["mapping"];

      isExcel(u_int) ? setMapping(mapping_data) : sessionStorage.setItem("wordData", JSON.stringify(mapping_data));; 
      const navigate_addres = isExcel(u_int) ? "/recoder" : "/questionnaireParser"
      
      setIsPopUp(false);
      navigate({ to: navigate_addres });
    }
  }

  return <> 
    <div className='flex flex-row'>
      <nav className='navbar w-full flex flex-row justify-around h-15 bg-[#181c24]'>
        <div className='flex flex-row justify-around items-center h-full w-125 z-1'>
        {[
        {nav_label:"Dashboard", to:"/dashboard"}, 
        {nav_label:"Kwestionariusz", to:"/questionnaireParser"},
        {nav_label:"Analiza", to:"/recoder"}].map((arr, i) => (
          <Link key={i} to={arr.to} className={`nav-option ${activeIndex === i ? "active" : ""} h-full w-30 flex justify-center`} onClick={() => {setActiveIndex(i)}}>
              <span className='text-[#8f96a8] h-full w-fit flex items-center select-none'>{arr.nav_label}</span>
          </Link>),
        )}
        </div>
        <div className='flex flex-row justify-around w-[20%]'>
          <Button className='px-6 py-2 self-center bg-[#E8821A] hover:bg-[#ff9d3a] text-white font-semibold rounded-lg transition-all duration-200 shadow-md active:scale-95 z-2' type='button' onClick={() => setIsPopUp(!isPopUp)}>Importuj plik</Button>
        </div>
        {isPopUp &&
          <div className='file-input-popup z-2 w-125 h-50 absolute top-[450%] right-[40%] bg-[#181c24] border-[#E8821A] border-2 rounded-[16px]'>
            <form className='h-full flex flex-col justify-around items-center' onSubmit={(e) => {handleSubmitFile(e)}}>
              <input id="file" name="file" type='file' className='bg-white w-5/6 px-4 border-none rounded-2xl' required></input>
              <div className='flex flex-row w-100 justify-evenly'>
                <Button className='w-[30%] h mb-2 self-center bg-[#E8821A] hover:bg-[#ff9d3a] text-white font-semibold rounded-lg transition-all duration-200 shadow-md active:scale-95 z-2' type='submit'>Dalej</Button>
                <Button className='w-[30%] h mb-2 self-center bg-[#111318] hover:bg-[#2f333e] text-white font-semibold rounded-lg transition-all duration-200 shadow-md active:scale-95 z-2' type='submit' onClick={() => setIsPopUp(!isPopUp)}>Wstecz</Button>
              </div>
            </form>
          </div>
        }
      </nav>
      <div className='divider'></div>
    </div>
    {activeIndex == 2 &&
    <Sidebar></Sidebar>
    }
  </>
}

