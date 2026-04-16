import { useMapping } from "@/context/MappingContext";

export const DownloadButton = () => {
    const { mapping, selectedCrosstables } = useMapping();

    const handleDatabaseDownload = async () => {
        if (!mapping) {
            console.error("Brak danych mappingu do wysłania");
            alert("Najpierw załaduj dane z pliku Excel!");
            return;
        }

        try {
            const payload = {
                mapping: mapping,
                crosstables: selectedCrosstables
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

    return (
        <button 
            onClick={handleDatabaseDownload}
            className="px-6 py-2 bg-[#E8821A] hover:bg-[#ff9d3a] text-white font-semibold rounded-lg transition-all duration-200 shadow-md active:scale-95"
        >
            Pobierz bazę (.zip)
        </button>
    );
};