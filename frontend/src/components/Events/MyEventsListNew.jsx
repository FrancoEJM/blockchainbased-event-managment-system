import { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { Button } from "flowbite-react";
import { HiOutlinePlus, HiTrash } from "react-icons/hi";
import DeleteEventButton from "./DeleteEventButton";
import StartEventButton from "./StartEventButton";
import QrCodeButton from "./QrCodeButton";
import QrReaderButton from "./QrReaderButton";
import EndEventButton from "./EndEventButton";
import StatsButton from "./StatsButton";

function MyEventsListNew({ user_id }) {
  const [events, setEvents] = useState(null);
  const [eventToDelete, setEventToDelete] = useState(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [qrUrl, setQrUrl] = useState(null);

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

  const handleDeleteSuccess = (event_id) => {
    const updatedEvents = events.filter(
      (evento) => evento.id_evento !== event_id
    );
    setEvents(updatedEvents);
  };

  const openConfirmModal = (event_id) => {
    setEventToDelete(event_id);
    setShowConfirmModal(true);
  };

  const closeConfirmModal = () => {
    setShowConfirmModal(false);
    setEventToDelete(null);
  };

  const handleStartEvent = async (
    event_id,
    execution_date,
    privacidad,
    array_qr_data = null
  ) => {
    if (privacidad == 1) {
      setEvents((prevEvents) =>
        prevEvents.map((evento) =>
          evento.id_evento == event_id
            ? {
                ...evento,
                fecha_ejecucion: execution_date,
                qrs_publicos: array_qr_data,
              }
            : evento
        )
      );
    }

    if (privacidad == 2) {
      setEvents((prevEvents) =>
        prevEvents.map((evento) =>
          evento.id_evento == event_id
            ? {
                ...evento,
                fecha_ejecucion: execution_date,
              }
            : evento
        )
      );
    }
  };

  const handleStartEventSuccess = (url) => {
    setQrUrl(url);
  };

  const handleEndEvent = async (event_id, end_date) => {
    setEvents((prevEvents) =>
      prevEvents.map((evento) =>
        evento.id_evento == event_id
          ? {
              ...evento,
              fecha_finalizacion: end_date,
            }
          : evento
      )
    );
  };

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_BACKEND_URL}/api/user/events`,
          {
            params: {
              user_id: user_id,
            },
          }
        );
        setEvents(response.data);
        console.log(response.data);
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };

    fetchEvents();
  }, [user_id]);
  return (
    <>
      <div className="mx-auto bg-gray-100 min-h-screen flex px-8 my-3">
        <div className="flex flex-col w-full items-center justify-center space-y-4">
          {events?.map((event) => (
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
                    {event.fecha_ejecucion == null && (
                      <>
                        <div className="w-1/2 flex justify-start ">
                          <Button
                            onClick={() => openConfirmModal(event.id_evento)}
                            className="ring-cyan-700 border border-gray-200 bg-white text-gray-900 focus:text-cyan-700 focus:ring-4 enabled:hover:bg-gray-100 enabled:hover:text-violet-700 dark:border-gray-600 dark:bg-transparent dark:text-gray-400 dark:enabled:hover:bg-gray-700 dark:enabled:hover:text-white"
                          >
                            {/* Texto visible en pantallas grandes */}
                            <span className="hidden sm:inline">
                              Eliminar evento
                            </span>

                            {/* Ícono visible en pantallas pequeñas */}
                            <span className="inline sm:hidden">
                              <HiTrash size={20} />{" "}
                              {/* Puedes ajustar el tamaño del ícono */}
                            </span>
                          </Button>
                        </div>
                        <div className="w-1/2 flex justify-end">
                          <StartEventButton
                            event={event}
                            onStartEvent={handleStartEvent}
                            onStartEventSuccess={handleStartEventSuccess}
                          />
                        </div>
                      </>
                    )}
                    {event.fecha_ejecucion != null && (
                      <div className="w-full">
                        {event.fecha_ejecucion != null &&
                          event.fecha_finalizacion == null && (
                            <div className="flex justify-between items-center">
                              <div>
                                {event.privacidad == 1 ? (
                                  <QrCodeButton
                                    events={events}
                                    event_id={event.id_evento}
                                  />
                                ) : (
                                  <QrReaderButton />
                                )}
                              </div>
                              <div className="ml-">
                                <EndEventButton
                                  event_id={event.id_evento}
                                  onEndEvent={handleEndEvent}
                                />
                              </div>
                            </div>
                          )}
                        {event.fecha_finalizacion != null && (
                          <StatsButton event_id={event.id_evento} />
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      {showConfirmModal && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-lg font-semibold">
              ¿Estás seguro de que deseas eliminar el evento?
            </h2>
            <p>Perderás toda la información relacionada. ¿Deseas continuar?</p>
            <div className="mt-4 flex justify-end">
              <button
                className="mr-2 py-2 px-4 bg-gray-300 rounded"
                onClick={closeConfirmModal}
              >
                No
              </button>
              <DeleteEventButton
                event_id={eventToDelete}
                onDeleteSuccess={handleDeleteSuccess}
                onCloseModal={closeConfirmModal}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}
export default MyEventsListNew;
