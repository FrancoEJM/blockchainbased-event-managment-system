import axios from "axios";
import { toast } from "react-toastify";

const DeleteEventButton = ({ event_id, onDeleteSuccess, onCloseModal }) => {
  const handleEventDelete = async () => {
    try {
      console.log("Deleting event with ID:", event_id);

      await axios.delete(`${import.meta.env.VITE_BACKEND_URL}/api/event`, {
        params: { event_id },
      });

      toast.success("El evento ha sido eliminado correctamente");

      // Llama a la función onDeleteSuccess para actualizar la lista de eventos
      onDeleteSuccess(event_id);

      // Cierra el modal de confirmación
      onCloseModal();
    } catch (error) {
      console.error("Error deleting event:", error);

      toast.error("Ha ocurrido un error al eliminar el evento");
    }
  };

  return (
    <button
      className="py-2 px-4 bg-red-500 text-white rounded"
      onClick={handleEventDelete}
    >
      Sí
    </button>
  );
};

export default DeleteEventButton;
