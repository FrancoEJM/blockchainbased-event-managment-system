import { useEffect, useState } from "react";
import axios from "axios";
import { formatDate, formatTime } from "../../utils/utils";
import Trash from "../icons/Trash";
import Edit from "../icons/Edit";
import StartEvent from "../icons/StartEvent";
import DeleteEventButton from "./DeleteEventButton";
import EndEvent from "../icons/EndEvent";
import StartEventButton from "./StartEventButton";
import QrCodeButton from "./QrCodeButton";
import EndEventButton from "./EndEventButton";
import StatsButton from "./StatsButton";

const MyEventsList = ({ user_id }) => {
  const [events, setEvents] = useState(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [eventToDelete, setEventToDelete] = useState(null);
  const [qrUrl, setQrUrl] = useState(null);

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

  const handleStartEventSuccess = (url) => {
    setQrUrl(url);
  };

  const handleStartEvent = async (event_id, execution_date, array_qr_data) => {
    setEvents((prevEvents) =>
      prevEvents.map((evento) =>
        evento.id_evento === event_id
          ? {
              ...evento,
              fecha_ejecucion: execution_date,
              qrs_publicos: array_qr_data,
            }
          : evento
      )
    );
  };

  const handleEndEvent = async (event_id, end_date) => {
    setEvents((prevEvents) =>
      prevEvents.map((evento) =>
        evento.id_evento === event_id
          ? {
              ...evento,
              fecha_finalizacion: end_date,
            }
          : evento
      )
    );
  };

  if (events === null) {
    return <div>Cargando eventos...</div>;
  }

  return (
    <>
      {events.map((evento) => (
        <div key={evento.id_evento} className="flex justify-center mx-5">
          <div className="w-full relative flex bg-clip-border bg-white text-gray-700 shadow-md max-w-6xl flex-row max-h-96 mt-5">
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
                {evento.descripcion && evento.descripcion.length < 170
                  ? evento.descripcion
                  : evento.descripcion
                  ? evento.descripcion.slice(0, 170) + "..."
                  : "Sin descripción"}
              </p>
              <div className="grid grid-cols-4 gap-4">
                <div className="col-span-2">
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
                <div className="col-span-2 col-start-3 row-span-3 flex items-center justify-end">
                  <button
                    className="mr-4"
                    title="Eliminar el evento"
                    onClick={() => openConfirmModal(evento.id_evento)}
                  >
                    {evento.fecha_ejecucion == null && <Trash />}
                  </button>
                  {evento.fecha_ejecucion == null &&
                    evento.fecha_finalizacion == null && (
                      <button className=" " title="Editar el evento">
                        <Edit />
                      </button>
                    )}

                  {evento.fecha_ejecucion == null && (
                    <StartEventButton
                      event={evento}
                      onStartEvent={handleStartEvent}
                      onStartEventSuccess={handleStartEventSuccess}
                    />
                  )}
                  {evento.fecha_ejecucion != null &&
                    evento.fecha_finalizacion == null && (
                      <>
                        <QrCodeButton
                          events={events}
                          event_id={evento.id_evento}
                        />
                        <EndEventButton
                          event_id={evento.id_evento}
                          onEndEvent={handleEndEvent}
                        />
                      </>
                    )}
                  {evento.fecha_finalizacion != null && (
                    <StatsButton event_id={evento.id_evento} />
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
