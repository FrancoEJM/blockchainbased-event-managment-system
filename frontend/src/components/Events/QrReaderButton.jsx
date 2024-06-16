import React, { useState } from "react";
import jsQR from "jsqr";

function QrReaderButton() {
  const [qrData, setQrData] = useState("");

  // Función para manejar la carga del archivo PNG
  const loadQRCode = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const image = new Image();
      image.onload = () => {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        canvas.width = image.width;
        canvas.height = image.height;
        ctx.drawImage(image, 0, 0, image.width, image.height);

        // Obtener los datos de píxeles de la imagen
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);

        if (code) {
          setQrData(code.data);
          try {
            const userData = JSON.parse(code.data.replace(/'/g, '"'));
            validateUser(userData);
            alert("Data del código QR leído:\n" + code.data);
          } catch (error) {
            console.error("Error al parsear JSON:", error + code.data);
            alert(
              "Error al parsear JSON. Verifica que el código QR sea válido."
            );
          }
        } else {
          alert("No se encontró un código QR válido en la imagen.");
        }
      };
      image.src = e.target.result;
    };
    reader.readAsDataURL(file);
  };

  const validateUser = async ({ event_id, email, token }) => {
    console.log(event_id, email, token);
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/user/validate_by_qr`,
        {},
        {
          params: {
            event_id: event_id,
            email: email,
            token: token,
          },
        }
      );
      if (response.status == 200) {
        console.log("response", response);
      }
    } catch (error) {
      console.error("Error starting event:", error);
    }
  };

  return (
    <div>
      <input type="file" accept="image/png" onChange={loadQRCode} />
      <br />
      <p>{qrData}</p>
    </div>
  );
}

export default QrReaderButton;
