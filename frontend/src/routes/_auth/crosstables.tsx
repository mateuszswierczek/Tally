import { createFileRoute } from '@tanstack/react-router'
import { Sidebar } from '../components/Subnavbar'
import { Navbar } from '../components/navbar'
import { MappingSchema } from '../-schemas';
import { z } from 'zod';
import { useMapping } from '@/context/MappingContext';

export const Route = createFileRoute('/_auth/crosstables')({
  component: Crosstable,
})
const Schema = MappingSchema;
const MapperSchema = z.array(Schema);

export function Crosstable() {
    const { mapping, setSelectedCrosstables, selectedCrosstables } = useMapping();

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const values = Array.from(e.target.selectedOptions, option => option.value);
        setSelectedCrosstables(values);
    };

    return (
        <div>
            <div className="p-10">
                <p className="text-white mb-4">Wybierz zmienne do tabel krzyżowych:</p>
                <select 
                    multiple 
                    className="w-full bg-[#181c24] text-white border border-[#2D3748] rounded-lg p-2"
                    value={selectedCrosstables} 
                    onChange={handleChange}
                >
                    {mapping?.map((item) => (
                        <option key={item.question} value={item.question}>
                            {item.question}
                        </option>
                    ))}
                </select>
                <p className="text-gray-400 mt-2">Wybrano: {selectedCrosstables.length}</p>
            </div>
        </div>
    );
}