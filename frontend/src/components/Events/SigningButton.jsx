import { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "flowbite-react";

function InscriptionButton({ event_id }) {
  const user_id = localStorage.getItem("id_usuario");
  const [isSigned, setIsSigned] = useState(false);
  const [loading, setLoading] = useState(true);
  const [hovering, setHovering] = useState(false);

  useEffect(() => {
    const checkIfSigned = async () => {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_BACKEND_URL}/api/user/is_signed`,
          {
            params: { event_id, user_id },
          }
        );
        setIsSigned(response.data);
      } catch (error) {
        console.error("Error checking sign-up status:", error);
      } finally {
        setLoading(false);
      }
    };

    checkIfSigned();
  }, [event_id, user_id]);

  const handleInscription = async () => {
    try {
      await axios.post(
        `${
          import.meta.env.VITE_BACKEND_URL
        }/api/user/inscription?event_id=${event_id}&user_id=${user_id}`
      );
      setIsSigned(true);
    } catch (error) {
      console.error("Error during inscription:", error);
    }
  };

  const handleUnsubscription = async () => {
    try {
      await axios.post(
        `${
          import.meta.env.VITE_BACKEND_URL
        }/api/user/unsubscribe?event_id=${event_id}&user_id=${user_id}`
      );
      setIsSigned(false);
    } catch (error) {
      console.error("Error during unsubscription:", error);
    }
  };

  if (loading) {
    return <p>Cargando...</p>;
  }

  return (
    <Button
      outline={true}
      color={hovering && isSigned ? "failure" : isSigned ? "success" : "purple"} // Rojo si está inscrito y en hover, verde si está inscrito, morado si no
      onClick={isSigned ? handleUnsubscription : handleInscription}
      onMouseEnter={() => setHovering(true)} // Activa el hover
      onMouseLeave={() => setHovering(false)} // Desactiva el hover
    >
      {hovering && isSigned
        ? "Darse de baja"
        : isSigned
        ? "Inscrito"
        : "Inscribirse"}
    </Button>
  );
}

export default InscriptionButton;
