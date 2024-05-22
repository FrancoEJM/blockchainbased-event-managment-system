// src/components/Events/utils.js

export const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("es-ES", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };
  
  export const formatTime = (timeString) => {
    const [hours,minutes] = timeString.split(":");
    return `${hours}:${minutes}`
  };
  