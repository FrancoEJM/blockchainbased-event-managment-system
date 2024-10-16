import { Button } from "flowbite-react";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { LuMapPin } from "react-icons/lu";
import SigningButton from "./SigningButton";

function EventDetail() {
  const [event, setEvent] = useState(null);
  const [isRegistered, setIsRegistered] = useState(false); // Estado para el botón
  const { id } = useParams();

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/api/event?id=${id}`
        );
        if (!response.ok) {
          throw new Error("Error al obtener el evento");
        }
        const data = await response.json();
        setEvent(data);
      } catch (error) {
        console.error("Error:", error);
      }
    };
    fetchEvents();
  }, [id]);

  if (!event) {
    return <p>Cargando...</p>;
  }

  // Extraer la fecha en formato adecuado
  const eventDate = new Date(event.fecha);
  const day = String(eventDate.getDate()).padStart(2, "0");
  const month = eventDate
    .toLocaleString("es-ES", { month: "short" })
    .toUpperCase();

  const getFormattedTime = (timeStrStart, timeStrEnd) => {
    const [hoursStart, minutesStart] = timeStrStart.split(":").map(Number);
    const [hoursEnd, minutesEnd] = timeStrEnd.split(":").map(Number);

    // Formatear las horas y minutos en formato de 24 horas
    const formattedHoursStart = hoursStart.toString().padStart(2, "0");
    const formattedHoursEnd = hoursEnd.toString().padStart(2, "0");

    return `${formattedHoursStart}:${minutesStart
      .toString()
      .padStart(2, "0")} - ${formattedHoursEnd}:${minutesEnd
      .toString()
      .padStart(2, "0")}`;
  };

  const handleRegistration = () => {
    setIsRegistered(!isRegistered);
  };

  return (
    <div className="max-w-lg rounded-lg overflow-hidden shadow-lg bg-white">
      <div
        className="relative h-64 bg-cover bg-center"
        style={{
          backgroundImage: `url(${import.meta.env.VITE_BACKEND_URL}${
            event.imagenes?.[0]?.path || "/default.jpg"
          })`,
        }}
      >
        <div className="absolute top-0 left-0 bg-white text-black p-2 rounded-br-lg">
          <span className="block text-xl font-bold">{day}</span>
          <span className="block text-sm">{month}</span>
        </div>
      </div>
      <div className="p-6">
        <div className="flex items-center mb-2">
          <span className="bg-violet-100 text-violet-800 text-xs font-medium inline-flex items-center px-2.5 py-0.5 rounded">
            {event.categorias?.descripcion || "Sin categoría"}
          </span>
        </div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">{event.nombre}</h3>
        <a
          href={`https://www.google.com/maps?q=${event.latitud},${event.longitud}`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-violet-500 mb-3 hover:underline cursor-pointer"
        >
          <span className="flex items-center mb-2">
            <LuMapPin className="inline-block align-middle" />
            <span className="ml-2 align-middle">
              {event.direccion || "Dirección no disponible"}
            </span>
          </span>
        </a>
        <p className="text-sm text-gray-500 mb-4">
          {eventDate.toLocaleDateString("es-ES", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
          })}{" "}
          - {getFormattedTime(event.hora_inicio, event.hora_fin)}
        </p>
        <p className="text-sm text-gray-500 mb-4">{event.descripcion}</p>
        <div className="flex justify-end">
          <SigningButton event_id={event.id_evento} />
        </div>
      </div>
    </div>
  );
}
export default EventDetail;
