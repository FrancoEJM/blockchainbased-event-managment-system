import React from "react";
import {
  PieChart,
  Pie,
  ResponsiveContainer,
  Cell,
  Legend,
  Tooltip,
} from "recharts";

function InvitationGraph({ event_stats }) {
  // Función para contar la cantidad de asistentes e invitados
  const countAttendees = () => {
    let attendeeCount = 0;
    let inviteeCount = 0;

    event_stats.detalles.forEach((participant) => {
      if (participant.invitado) {
        inviteeCount++;
      } else {
        attendeeCount++;
      }
    });

    return { attendees: attendeeCount, invitees: inviteeCount };
  };

  // Datos para el gráfico de torta
  const { attendees, invitees } = countAttendees();

  const data = [
    { name: "Asistentes", value: attendees },
    { name: "Invitados", value: invitees },
  ];

  const COLORS = ["#b3aaeb", "#968aec"];

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
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export default InvitationGraph;
