import React, { useState, useEffect } from "react";
import { ButtonGroup, Button } from "flowbite-react";
import { HiOutlinePlus } from "react-icons/hi";
import NavbarTest from "../../components/NavbarTest";
import "../../styles/eventspage.css";
import { Link } from "react-router-dom";

// Función para formatear la fecha en el formato deseado
const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  const options = { month: "short", day: "numeric", year: "numeric" };
  return date.toLocaleDateString("es-ES", options);
};

// Función para obtener el nombre del mes en español
const getMonthName = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString("es-ES", { month: "short" }).toUpperCase();
};

// Función para obtener la hora en formato de 12 horas
const getFormattedTime = (timeStrStart, timeStrEnd) => {
  const [hoursStart, minutesStart] = timeStrStart.split(":");
  const [hoursEnd, minutesEnd] = timeStrEnd.split(":");
  const formattedHoursStart = hoursStart % 12 || 12;
  const formattedHoursEnd = hoursEnd % 12 || 12;
  return `${formattedHoursStart}:${minutesStart} - ${formattedHoursEnd}:${minutesEnd}`;
};

const truncateDescription = (description) => {
  return description && description.length > 150
    ? description.substring(0, 150) + "..."
    : description;
};

function EventsListText() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const user_id = localStorage.getItem("id_usuario");
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/api/events?id=${user_id}`
        );
        if (!response.ok) {
          throw new Error("Error al obtener los eventos");
        }
        const data = await response.json();
        setEvents(data);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchEvents();
  }, []);

  return (
    <>
      <NavbarTest />
      <div className="mx-auto bg-gray-100 min-h-screen flex px-8 my-3">
        <div className="flex flex-col w-full items-center justify-center space-y-4">
          {events.map((event) => (
            <div
              key={event.id_evento}
              className="flex flex-col w-full bg-white rounded-lg shadow-lg sm:w-3/4 md:w-1/2 lg:w-3/5"
            >
              <div
                className="w-full h-64 bg-top bg-cover rounded-t-lg"
                style={{
                  backgroundImage: `url(${import.meta.env.VITE_BACKEND_URL}${
                    event.imagenes[0]?.path || "/default.jpg"
                  })`,
                }}
              ></div>
              <div className="flex flex-col w-full md:flex-row">
                <div className="flex flex-row justify-around p-4 font-bold leading-none text-violet-700 uppercase bg-violet-300 md:flex-col md:items-center md:justify-center md:w-1/4 md:rounded-bl-lg">
                  <div className="md:text-3xl">{getMonthName(event.fecha)}</div>
                  <div className="md:text-6xl">
                    {new Date(event.fecha).getDate()}
                  </div>
                  <div className="md:text-xl">
                    {getFormattedTime(event.hora_inicio, event.hora_fin)}
                  </div>
                </div>
                <div className="p-4 font-normal text-gray-800 md:w-3/4">
                  <h1 className="mb-4 text-4xl font-bold leading-none tracking-tight text-gray-800">
                    {event.nombre}
                  </h1>
                  <p className="truncate-lines">
                    {/* {truncateDescription(event.descripcion)} */}
                    {event.descripcion}
                  </p>
                  <div className="flex flex-row items-center mt-4 text-gray-700">
                    <div className="w-1/2 font-semibold uppercase">
                      {event.categorias.descripcion}
                    </div>
                    <div className="w-1/2 flex justify-end">
                      {/* <ButtonGroup> */}
                      <Link to={`/event-new/${event.id_evento}`}>
                        <Button className="ring-cyan-700 border border-gray-200 bg-white text-gray-900 focus:text-cyan-700 focus:ring-4 enabled:hover:bg-gray-100 enabled:hover:text-violet-700 dark:border-gray-600 dark:bg-transparent dark:text-gray-400 dark:enabled:hover:bg-gray-700 dark:enabled:hover:text-white">
                          <span className="hidden sm:inline">
                            Quiero saber más
                          </span>
                          <span className="sm:hidden mt-1">
                            <HiOutlinePlus />
                          </span>
                        </Button>
                      </Link>
                      {/* <Button className="ring-cyan-700 border border-gray-200 bg-white text-gray-900 focus:text-cyan-700 focus:ring-4 enabled:hover:bg-gray-100 enabled:hover:text-violet-700 dark:border-gray-600 dark:bg-transparent dark:text-gray-400 dark:enabled:hover:bg-gray-700 dark:enabled:hover:text-white">
                          Inscribirme
                        </Button> */}
                      {/* </ButtonGroup> */}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default EventsListText;
