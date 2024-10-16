import axios from "axios";
import { Button } from "flowbite-react";
import { useState } from "react";

function EndEventButton({ event_id, onEndEvent }) {
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  const handleEventFinish = async () => {
    setShowConfirmModal(true);
  };

  const handleConfirmFinish = async () => {
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/event/end`,
        {},
        {
          params: {
            event_id: event_id,
          },
        }
      );
      if (response.status === 200) {
        console.log("El evento ha finalizado correctamente", response);
        const end_date = response.data.fecha_finalizacion;
        onEndEvent(event_id, end_date);
      }
    } catch (error) {
      console.error("Error ending event:", error);
    } finally {
      setShowConfirmModal(false); // Cierra el modal de confirmación después de finalizar
    }
  };

  const handleCloseModal = () => {
    setShowConfirmModal(false);
  };

  return (
    <>
      <Button
        onClick={handleEventFinish}
        className=" ring-cyan-700 border border-gray-200 bg-white text-gray-900 focus:text-cyan-700 focus:ring-4 enabled:hover:bg-gray-100 enabled:hover:text-violet-700 dark:border-gray-600 dark:bg-transparent dark:text-gray-400 dark:enabled:hover:bg-gray-700 dark:enabled:hover:text-white"
      >
        <div className="flex items-center">
          <div className="hidden sm:block mr-1">Finalizar el evento</div>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="icon icon-tabler icon-tabler-clock-12"
            width="30"
            height="30"
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
        </div>
      </Button>
      {/* <button
        className="p-4 ml-4 bg-green-100 rounded-full"
        title="Finalizar el evento"
        onClick={handleEventFinish}
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
      </button> */}

      {showConfirmModal && (
        <div
          className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
          onClick={handleCloseModal}
        >
          <div className="bg-white p-8 rounded shadow-lg max-w-xs mx-auto">
            <div className="font-medium">
              ¿Seguro que desea finalizar el evento?
            </div>
            <div>Esta acción es irreversible.</div>
            <div className="mt-4 flex justify-between">
              <button
                className="mr-2 bg-gray-200 text-gray-700 px-4 py-2 rounded"
                onClick={handleCloseModal}
              >
                Cancelar
              </button>
              <button
                className="bg-red-500 text-white px-4 py-2 rounded"
                onClick={handleConfirmFinish}
              >
                Continuar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default EndEventButton;
