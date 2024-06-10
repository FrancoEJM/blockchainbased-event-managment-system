import axios from "axios";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import GenderGraph from "./GenderGraph";
import AgeGraph from "./AgeGraph";
import InvitationGraph from "./InvitationGraph";

function EventDisplayStats() {
  const [eventName, setEventName] = useState("");
  const [eventStats, setEventStats] = useState(null);
  const { event_id } = useParams();

  useEffect(() => {
    const fetchEventStats = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_BACKEND_URL}/api/event/stats`,
          {
            params: {
              event_id: event_id,
            },
          }
        );
        setEventStats(response.data);
      } catch (error) {
        console.error("Error fetching stats", error);
      }
    };

    const fetchEventName = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_BACKEND_URL}/api/event/`,
          {
            params: {
              id: event_id,
            },
          }
        );
        setEventName(response.data.nombre);
      } catch (error) {
        console.error("Error fetching event", error);
      }
    };

    fetchEventStats();
    fetchEventName();
  }, [event_id]);

  if (!eventStats || !eventName) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex items-start justify-center h-screen mt-10">
      <div className="bg-white w-full max-w-5xl px-10 py-10 shadow-lg border-2 border-gray-200">
        <h1 className="text-2xl font-semibold text-center">
          Felicidades, tu evento "{eventName}" ha tenido{" "}
          {eventStats.numero_registros} asistentes
        </h1>
        <div className="grid grid-cols-9 gap-4 mt-5">
          <div className="col-span-2">
            <div className="flex items-center justify-center ">Género</div>
            <GenderGraph gender_stats={eventStats.detalles} />
          </div>
          <div className="col-span-5">
            <div className="flex items-center justify-center ">Edad</div>
            <AgeGraph age_stats={eventStats.detalles} />
          </div>
          <div className="col-span-2 ml-3">
            <div className="flex items-center justify-center">
              Invitados y asistentes
            </div>
            <InvitationGraph event_stats={eventStats} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default EventDisplayStats;
