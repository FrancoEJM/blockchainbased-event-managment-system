import React from "react";
import {
  PieChart,
  Pie,
  ResponsiveContainer,
  Cell,
  Legend,
  Tooltip,
} from "recharts";

const COLORS = ["#6d63bc", "#c4c2f3", "#b3aaeb", "#968aec", "#797dd6"];

function GeneralAttendeeStats({ attendee_stats }) {
  // Agrupar por id_evento y contar el número de asistentes por evento
  const countAttendeesByEvent = () => {
    const eventCounts = {};

    attendee_stats.forEach((attendee) => {
      const { id_evento, nombre_evento } = attendee;

      if (eventCounts[id_evento]) {
        eventCounts[id_evento].value++;
      } else {
        eventCounts[id_evento] = {
          name: nombre_evento,
          value: 1,
        };
      }
    });

    // Convertir a array y ordenar por el número de asistentes (value)
    const data = Object.values(eventCounts).sort((a, b) => b.value - a.value);

    return data;
  };

  const data = countAttendeesByEvent();

  // Obtener solo los 4 primeros eventos para la leyenda
  const legendData = data.slice(0, 4);
  // Obtener el payload para la leyenda
  const legendPayload = legendData.map((entry, index) => ({
    value: entry.name,
    type: "square",
    color: COLORS[index % COLORS.length],
  }));

  return (
    <div style={{ width: "100%", height: 300 }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={80}
            fill="#8884d8"
            label
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip />
          <Legend payload={legendPayload} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default GeneralAttendeeStats;
