import StartEvent from "../icons/StartEvent";
import axios from "axios";

function StartEventButton({ event, onStartEvent, onStartEventSuccess }) {
  const startPublicEvent = async () => {
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/event/start`,
        {},
        {
          params: {
            event_id: event.id_evento,
          },
        }
      );
      if (response.status == 200) {
        console.log("response", response);
        const execution_date = response.data[0];
        const qr_path = response.data[1];
        const array_qr_data = [
          {
            path: qr_path,
            id_evento: event.id_evento,
            id_qr: event.id_evento,
          },
        ];

        //onStartEventSuccess(qr_path);
        onStartEvent(
          event.id_evento,
          execution_date,
          event.privacidad,
          array_qr_data
        );
      }
    } catch (error) {
      console.error("Error starting event:", error);
    }
  };

  const startPrivateEvent = async () => {
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/event/start`,
        {},
        {
          params: {
            event_id: event.id_evento,
          },
        }
      );
      if (response.status == 200) {
        const execution_date = response.data[0];
        console.log(
          "El evento ha comenzado correctamente",
          execution_date,
          response
        );
        onStartEvent(event.id_evento, execution_date, event.privacidad);
      }
    } catch (error) {
      console.error("Error starting event", error);
    }
  };
  return (
    <button
      className="p-4 ml-4 bg-violet-300 rounded-full"
      title="Comenzar el evento"
      onClick={event.privacidad == 1 ? startPublicEvent : startPrivateEvent}
    >
      <StartEvent />
    </button>
  );
}
export default StartEventButton;
