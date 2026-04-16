import { createContext, useContext, useState, ReactNode, Dispatch, SetStateAction } from 'react';
import { z } from 'zod';
import { MappingSchema } from '@/routes/-schemas';

const MapperSchema = z.array(MappingSchema);
type Mapping = z.infer<typeof MapperSchema>;

interface MappingContextType {
    mapping: Mapping | null;
    setMapping: Dispatch<SetStateAction<Mapping | null>>;
    selectedCrosstables: string[];
    setSelectedCrosstables: Dispatch<SetStateAction<string[]>>;
}

const MappingContext = createContext<MappingContextType | undefined>(undefined);

export function MappingProvider({ children }: { children: ReactNode }) {
    const [mapping, setMapping] = useState<Mapping | null>(() => {
        if (typeof window === 'undefined') return null;

        const stored = sessionStorage.getItem('excelData');
        if (!stored) return null;

        try {
            const parsed = JSON.parse(stored);
            const result = MapperSchema.safeParse(parsed);
            
            if (result.success) {
                return result.data;
            } else {
                console.error("Błąd walidacji danych z sessionStorage:", result.error.issues);
                return null;
            }
        } catch (error) {
            console.error("Błąd parsowania danych z sessionStorage:", error);
            return null;
        }
    });

    const [selectedCrosstables, setSelectedCrosstables] = useState<string[]>([]);

    return (
        <MappingContext.Provider 
            value={{ 
                mapping, 
                setMapping, 
                selectedCrosstables, 
                setSelectedCrosstables 
            }}
        >
            {children}
        </MappingContext.Provider>
    );
}

export const useMapping = () => {
    const context = useContext(MappingContext);
    if (!context) {
        throw new Error("useMapping must be used within MappingProvider");
    }
    return context;
};