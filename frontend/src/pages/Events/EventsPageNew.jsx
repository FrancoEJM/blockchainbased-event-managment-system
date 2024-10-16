import { Button } from "primereact/button";
import { Card } from "primereact/card";
import NavbarNew from "../../components/NavbarNew";
import "../../styles/eventspage.css";

// const [events, setEvents] = useState([]);
// const user_id = localStorage.id_usuario;
// const URL = import.meta.env.VITE_BACKEND_URL;
// useEffect(() => {
//   const fetchEvents = async () => {
//     try {
//       const response = await fetch(`${URL}/api/events?id=${user_id}`);
//       if (!response.ok) {
//         throw new Error("Error al obtener los eventos");
//       }
//       const data = await response.json();
//       setEvents(data);
//     } catch (error) {
//       console.error("Error:", error);
//     }
//   };

//   fetchEvents();
// }, []);

function EventsPageNew() {
  const header = (
    <img
      alt="Card"
      src="https://primefaces.org/cdn/primereact/images/usercard.png"
    />
  );
  const footer = (
    <>
      <Button label="Save" icon="pi pi-check" />
      <Button
        label="Cancel"
        severity="secondary"
        icon="pi pi-times"
        style={{ marginLeft: "0.5em" }}
      />
      <Button label="Save" icon="pi pi-check" />
    </>
  );
  return (
    <div>
      <NavbarNew />
      <Card
        title="Advanced Card"
        subTitle="Card subtitle"
        header={header}
        className="md:w-25rem"
      >
        <p className="m-0">
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Inventore
          sed consequuntur error repudiandae numquam deserunt quisquam repellat
          libero asperiores earum nam nobis, culpa ratione quam perferendis
          esse, cupiditate neque quas!
        </p>
        <div className="buttons-container">
          <Button label="Save" />
          <Button label="Save" />
        </div>
      </Card>
    </div>
  );
}
export default EventsPageNew;
