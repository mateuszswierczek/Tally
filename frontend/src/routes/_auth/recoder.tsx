import { createFileRoute } from '@tanstack/react-router'
import { Navbar } from '../components/navbar'
import { useState } from 'react'
import { useEffect } from 'react'
import { MappingSchema } from '../schemas'
import { z } from 'zod';
import './navbar.css'

export const Route = createFileRoute('/_auth/recoder')({
  component: RouteComponent,
})
const MapperSchema = z.array(MappingSchema);
type Mapping = z.infer<typeof MapperSchema>;


function RouteComponent() {
    const [mapping, setMapping] = useState<Mapping | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const stored = sessionStorage.getItem('excelData');

        if (!stored) {
            console.log("error: brak danych");
            return;
        }

        const result = MapperSchema.safeParse(JSON.parse(stored)); // ← JSON.parse!

        if (result.success) {
            setMapping(result.data);
        } else {
            setError(result.error.toString());
            console.error(result.error.issues); // pokaże dokładnie co się nie zgadza
        }
    }, []);

    if (error) return <p style={{ color: "red" }}>{error}</p>;
    if (!mapping) return <p>Ładowanie...</p>;

    return (
        <>
            <Navbar />
            {Object.values(mapping).map((item, i) => (
                <div key={i}>
                    <p>Question: {item.question}</p>
                    <div>
                        {item.cafeteria?.map((c) => {
  console.log(c); // check the browser console
  return (
    <div key={c.index}>
      {c.value}
    </div>
  );
})}
                        
                    </div>
                </div>
            ))}
        </>
    );
}
