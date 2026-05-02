import { useMapping } from "@/context/MappingContext";
import { useState } from "react";
import { fa } from "zod/v4/locales";

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
        {/* TODO: Poprawić ten popup */}
        {isPopUp &&
            <div className="text-white">
                <label htmlFor="merged">Złączone tabele?</label>
                <input id="merged" onChange={(_) => setIsMergedTables(!isMergedTables)}></input>
                <button onClick={handleDatabaseDownload}>Dalej</button>
            </div>
        }
    </div>

    );
};