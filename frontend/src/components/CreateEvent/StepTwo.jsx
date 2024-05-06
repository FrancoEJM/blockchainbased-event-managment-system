/* eslint-disable react/prop-types */
import { useState } from "react";
import arte from "../../assets/categorias/arte_y_cultura.png";
import deportes from "../../assets/categorias/deportes.png";
import educacion from "../../assets/categorias/educacion.png";
import entretenimiento from "../../assets/categorias/entretenimiento.png";
import gastronomia from "../../assets/categorias/gastronomia.png";
import musica from "../../assets/categorias/musica.png";
import negocios from "../../assets/categorias/negocios.png";
import tecnologia from "../../assets/categorias/tecnologia.png";
import viajes from "../../assets/categorias/viajes.png";

function StepTwo({ onChange }) {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const categories = [
    { id: 1, name: "Arte y Cultura", image: arte },
    { id: 2, name: "Deportes", image: deportes },
    { id: 3, name: "Educación", image: educacion },
    { id: 4, name: "Entretenimiento", image: entretenimiento },
    { id: 5, name: "Gastronomía", image: gastronomia },
    { id: 6, name: "Música", image: musica },
    { id: 7, name: "Negocios", image: negocios },
    { id: 8, name: "Tecnología", image: tecnologia },
    { id: 9, name: "Viajes", image: viajes },
  ];

  const handleCategoryClick = (categoryId) => {
    setSelectedCategory(categoryId);
    onChange(categoryId);
  };

  return (
    <div className="grid grid-cols-3 gap-4">
      {categories.map((category) => (
        <div
          key={category.id}
          className={`${
            selectedCategory === category.id
              ? "bg-violet-300 shadow-2xl"
              : "bg-gray-200"
          } shadow-md p-4 flex flex-col items-center justify-center text-center cursor-pointer`}
          onClick={() => handleCategoryClick(category.id)}
        >
          <img
            src={category.image}
            alt={category.name}
            className="w-24 h-24 object-cover mb-2"
          />
          <span className="text-md font-medium font-mono">{category.name}</span>
        </div>
      ))}
    </div>
  );
}

export default StepTwo;
