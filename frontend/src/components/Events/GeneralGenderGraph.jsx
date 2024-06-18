import React from "react";
import {
  PieChart,
  Pie,
  ResponsiveContainer,
  Cell,
  Legend,
  Tooltip,
} from "recharts";

const GENDER_MAP = {
  0: "Desconocido",
  1: "Masculino",
  2: "Femenino",
  3: "Otro",
  4: "Prefiero no responder",
};

const COLORS = ["#6d63bc", "#c4c2f3", "#b3aaeb", "#968aec", "#797dd6"];

function GeneralGenderGraph({ gender_stats }) {
  // Función para contar la cantidad de cada género
  const countGenders = () => {
    let genderCounts = {};

    // Contar cada género
    gender_stats.forEach((participant) => {
      const gender = GENDER_MAP[participant.genero];
      if (genderCounts[gender]) {
        genderCounts[gender]++;
      } else {
        genderCounts[gender] = 1;
      }
    });

    // Preparar datos para el gráfico de torta
    const data = Object.keys(genderCounts).map((gender) => ({
      name: gender,
      value: genderCounts[gender],
    }));

    return data;
  };

  // Datos para el gráfico de torta
  const data = countGenders();

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

export default GeneralGenderGraph;
