import { createFileRoute } from '@tanstack/react-router'
import { useSelectionContainer } from '@air/react-drag-to-select'


export const Route = createFileRoute('/_auth/db_creator')({
  component: DBCreator,
})

function DBCreator() {
    const { DragSelection } = useSelectionContainer();
    return <div>
        <DragSelection/>
        <div className='text-white'>Element</div>
    </div>
}
