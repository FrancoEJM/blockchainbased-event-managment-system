import { useParams } from "react-router-dom";
import DataCollectionForm from "../../components/DataCollection/DataCollectionForm";
function DataCollection() {
  const { event_id } = useParams();
  return (
    <div>
      <DataCollectionForm event_id={event_id} />
    </div>
  );
}
export default DataCollection;
