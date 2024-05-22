import React, { useState, useEffect } from "react";
import axios from "axios";

function EventSigningButton({ event_id }) {
  const user_id = localStorage.getItem("id_usuario");

  const [isSigned, setIsSigned] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkIfSigned = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/api/user/is_signed`, {
          params: { event_id, user_id }
        });
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
      await axios.post(`${import.meta.env.VITE_BACKEND_URL}/api/user/inscription?event_id=${event_id}&user_id=${user_id}`);
      setIsSigned(true);
    } catch (error) {
      console.error("Error during inscription:", error);
    }
  };

  const handleUnsubscription = async () => {
    try {
      await axios.post(`${import.meta.env.VITE_BACKEND_URL}/api/user/unsubscribe?event_id=${event_id}&user_id=${user_id}`);
      setIsSigned(false);
    } catch (error) {
      console.error("Error during unsubscription:", error);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return isSigned ? (
    <button
      className="bg-red-500 hover:bg-red-400 text-white font-bold py-2 px-4 border-b-4 border-red-800 hover:border-red-500 shadow-md"
      onClick={handleUnsubscription}
    >
      - Desinscribirse
    </button>
  ) : (
    <button
      className="bg-violet-500 hover:bg-violet-400 text-white font-bold py-2 px-4 border-b-4 border-violet-800 hover:border-violet-500 shadow-md"
      onClick={handleInscription}
    >
      + Inscribirse
    </button>
  );
}

export default EventSigningButton;
