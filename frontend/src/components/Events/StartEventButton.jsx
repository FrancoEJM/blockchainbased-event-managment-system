import StartEvent from "../icons/StartEvent";
import axios from "axios";
import { Button } from "flowbite-react";
import { HiPlay } from "react-icons/hi";

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
    // <button
    //   className="p-4 ml-4 bg-violet-300 rounded-full"
    //   title="Comenzar el evento"
    // >
    //   <StartEvent />
    // </button>

    <Button
      onClick={event.privacidad === 1 ? startPublicEvent : startPrivateEvent}
      className="ring-cyan-700 border border-gray-200 bg-white text-gray-900 focus:text-cyan-700 focus:ring-4 enabled:hover:bg-gray-100 enabled:hover:text-violet-700 dark:border-gray-600 dark:bg-transparent dark:text-gray-400 dark:enabled:hover:bg-gray-700 dark:enabled:hover:text-white"
    >
      {/* Texto visible solo en pantallas grandes */}
      <span className="hidden sm:inline">Iniciar Evento</span>

      {/* Ícono visible solo en pantallas pequeñas */}
      <span className="inline sm:hidden">
        <HiPlay size={20} /> {/* Ajusta el tamaño del ícono si es necesario */}
      </span>
    </Button>
  );
}
export default StartEventButton;
