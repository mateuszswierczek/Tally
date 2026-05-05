import { useMapping } from "@/context/MappingContext";
import { useState } from "react";

export const DownloadButton = () => {
    const { mapping, selectedCrosstables } = useMapping();
    const [ isPopUp, setIsPopUp ] = useState<boolean>(false);
    const [ isMergedTables, setIsMergedTables ] = useState<boolean>(false);

    function handleIsPopUp() {
        setIsPopUp(!isPopUp)
    }

    const handleDatabaseDownload = async () => {
        if (!mapping) {
            console.error("Brak danych mappingu do wysłania");
            alert("Najpierw załaduj dane z pliku Excel!");
            return;
        }

        try {
            const payload = {
                mapping: mapping,
                crosstables: selectedCrosstables,
                merged: isMergedTables
            };

            const req = await fetch("http://127.0.0.1:8000/api/post_mapping", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                },
                body: JSON.stringify(payload),
            });

            if (!req.ok) {
                const errorData = await req.json().catch(() => ({}));
                console.error("Błąd serwera:", errorData);
                alert("Wystąpił błąd podczas generowania bazy.");
                return;
            }

            const file = await req.blob();
            const download_url = URL.createObjectURL(file);
            const link = document.createElement('a');

            link.href = download_url;
            link.download = 'Baza.zip';
            document.body.appendChild(link);             
            link.click();
            document.body.removeChild(link);
            
            URL.revokeObjectURL(download_url);

        } catch (err) {
            console.error("Błąd sieci:", err);
            alert("Nie udało się połączyć z serwerem.");
        }
    };

    return (<div>
        <button 
            onClick={handleIsPopUp}
            className="px-6 py-2 bg-[#E8821A] hover:bg-[#ff9d3a] text-white font-semibold rounded-lg transition-all duration-200 shadow-md active:scale-95 z-2"
        >
            Pobierz bazę (.zip)
        </button>
        {isPopUp &&
            <div className="text-white absolute bg-[#181c24] border-2 border-[#2D3748] w-75 h-75 bottom-[50%] left-[40%] flex flex-col justify-between">
                <div>
                    <h1 className="text-center text-xl mb-2">Opcje:</h1>
                    <div className="flex justify-around">
                        <label htmlFor="merged">Złączone tabele?</label>
                        <input id="merged" type="checkbox" onChange={() => setIsMergedTables(!isMergedTables)} checked={isMergedTables}/>
                    </div>
                </div>
                <div className="flex flex-row justify-around">
                    <button className="w-[40%] h mb-2 self-center bg-[#E8821A] hover:bg-[#ff9d3a] text-white font-semibold rounded-lg transition-all duration-200 shadow-md active:scale-95 z-2" onClick={handleDatabaseDownload}>Dalej</button>
                    <button className="w-[40%] h mb-2 self-center bg-[#111318] hover:bg-[#2f333e] text-white font-semibold rounded-lg transition-all duration-200 shadow-md active:scale-95 z-2" onClick={() => setIsPopUp(!isPopUp)}>Wstecz</button>
                </div>
            </div>
        }
    </div>

    );
};