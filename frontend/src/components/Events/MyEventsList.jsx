import { useEffect, useState } from "react";
import axios from "axios";
import { formatDate, formatTime } from "../../utils/utils";
import Trash from "../icons/Trash";
import Edit from "../icons/Edit";
import StartEvent from "../icons/StartEvent";
import DeleteEventButton from "./DeleteEventButton";
import EndEvent from "../icons/EndEvent";

const MyEventsList = ({ user_id }) => {
  const [events, setEvents] = useState(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [eventToDelete, setEventToDelete] = useState(null);

  useEffect(() => {
    console.log("sucede el useEffect");
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

        console.log(response.data);
        setEvents(response.data);
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };

    fetchEvents();
  }, [user_id]);

  const openConfirmModal = (event_id) => {
    setEventToDelete(event_id);
    setShowConfirmModal(true);
  };

  const closeConfirmModal = () => {
    setShowConfirmModal(false);
    setEventToDelete(null);
  };

  const handleDeleteSuccess = (event_id) => {
    const updatedEvents = events.filter(
      (evento) => evento.id_evento !== event_id
    );
    setEvents(updatedEvents);
  };

  if (events === null) {
    return <div>Cargando eventos...</div>; // Mensaje de carga mientras se obtienen los datos
  }

  return (
    <>
      {events.map((evento) => (
        <div key={evento.id_evento} className="flex justify-center mx-5">
          <div className="w-full relative flex bg-clip-border bg-white text-gray-700 shadow-md max-w-6xl flex-row max-h-80 mt-5">
            <div className="relative w-2/5 m-0 overflow-hidden text-gray-700 bg-white rounded-r-none bg-clip-border shrink-0">
              {evento.imagenes.length > 0 && (
                <img
                  src={`${import.meta.env.VITE_BACKEND_URL}${
                    evento.imagenes[0].path
                  }`}
                  alt="card-image"
                  className="object-cover w-full h-full"
                />
              )}
            </div>
            <div className="p-6">
              <h6
                id="category"
                className="block mb-4 font-sans text-base antialiased font-semibold leading-relaxed tracking-normal text-gray-700 uppercase"
              >
                {evento.categorias.descripcion}
              </h6>
              <h4
                id="title"
                className="block mb-2 font-sans text-2xl antialiased font-semibold leading-snug tracking-normal text-blue-gray-900"
              >
                {evento.nombre}
              </h4>
              <p
                id="text"
                className="block mb-4 font-sans text-base antialiased font-normal leading-relaxed text-gray-700"
              >
                {evento.descripcion.length < 170
                  ? evento.descripcion
                  : evento.descripcion.slice(0, 170) + "..."}
              </p>
              <div className="grid grid-cols-4 gap-4">
                <div className="col-span-3">
                  <div className="grid grid-rows-4 gap-2">
                    <div className="row-span-1 flex items-center">
                      <div className="font-semibold">Fecha:</div>
                      <div id="date" className="ml-2">
                        {formatDate(evento.fecha)}
                      </div>
                    </div>
                    <div className="row-span-1 flex items-center">
                      <div className="font-semibold">Hora:</div>
                      <div id="hour" className="ml-2">
                        {formatTime(evento.hora_inicio)} -{" "}
                        {formatTime(evento.hora_fin)}
                      </div>
                    </div>
                    <div className="row-span-1 flex items-center">
                      {evento.modalidades && (
                        <>
                          <div className="font-semibold">Modalidad:</div>
                          <div
                            id={`modalidad-${evento.modalidades.id_modalidad}`}
                            className="ml-1"
                          >
                            {evento.modalidades.descripcion}
                          </div>
                          {evento.modalidades.id_modalidad === 1 &&
                            evento.direccion && (
                              <>
                                <div className="font-semibold ml-4">
                                  Dirección:
                                </div>
                                <div className="ml-1">{evento.direccion}</div>
                              </>
                            )}
                        </>
                      )}
                    </div>
                  </div>
                </div>
                <div className="col-span-1 row-span-3 items-center justify-between">
                  <button
                    className="py-4"
                    title="Eliminar el evento"
                    onClick={() => openConfirmModal(evento.id_evento)}
                  >
                    <Trash />
                  </button>
                  {evento.fecha_ejecucion == null &&
                    evento.fecha_finalizacion == null && (
                      <button className="py-4 mx-1" title="Editar el evento">
                        <Edit />
                      </button>
                    )}

                  {evento.fecha_ejecucion == null && (
                    <button
                      className="p-4 ml-4 bg-violet-300 rounded-full"
                      title="Comenzar el evento"
                    >
                      <StartEvent />
                    </button>
                  )}
                  {evento.fecha_ejecucion != null &&
                    evento.fecha_finalizacion == null && (
                      <button
                        className="p-4 ml-4 bg-green-100 rounded-full"
                        title="Finalizar el evento"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          className="icon icon-tabler icon-tabler-clock-12"
                          width="24"
                          height="24"
                          viewBox="0 0 24 24"
                          strokeWidth="1.5"
                          stroke="#2c3e50"
                          fill="none"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                          <path d="M3 12a9 9 0 0 0 9 9m9 -9a9 9 0 1 0 -18 0" />
                          <path d="M12 7v5l.5 .5" />
                          <path d="M18 15h2a1 1 0 0 1 1 1v1a1 1 0 0 1 -1 1h-1a1 1 0 0 0 -1 1v1a1 1 0 0 0 1 1h2" />
                          <path d="M15 21v-6" />
                        </svg>
                      </button>
                    )}
                  {evento.fecha_finalizacion != null && (
                    <button
                      className="p-4 ml-4 bg-red-100 rounded-full"
                      title="Ver estadísticas"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        class="icon icon-tabler icon-tabler-device-desktop-analytics"
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                        stroke="#2c3e50"
                        fill="none"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      >
                        <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                        <path d="M3 4m0 1a1 1 0 0 1 1 -1h16a1 1 0 0 1 1 1v10a1 1 0 0 1 -1 1h-16a1 1 0 0 1 -1 -1z" />
                        <path d="M7 20h10" />
                        <path d="M9 16v4" />
                        <path d="M15 16v4" />
                        <path d="M9 12v-4" />
                        <path d="M12 12v-1" />
                        <path d="M15 12v-2" />
                        <path d="M12 12v-1" />
                      </svg>
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}

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
};

export default MyEventsList;
