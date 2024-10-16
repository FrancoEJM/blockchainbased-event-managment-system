import { Menubar } from "primereact/menubar";
import "../styles/navbar.css";
const items = [
  {
    label: "Mi información",
    icon: "pi pi-user",
    items: [
      {
        label: "Perfil",
        icon: "pi pi-id-card",
      },
      {
        label: "Cerrar sesión",
        icon: "pi pi-sign-out",
      },
    ],
  },
  {
    label: "Eventos",
    icon: "pi pi-calendar",
    items: [
      {
        label: "Mis eventos",
        icon: "pi pi-list",
      },
      {
        label: "Eventos realizados",
        icon: "pi pi-history",
      },
      {
        label: "Estadísticas",
        icon: "pi pi-chart-bar",
      },
    ],
  },
  {
    label: "Crea un nuevo evento",
    icon: "pi pi-plus-circle",
  },
];

function NavbarNew() {
  return (
    <div className="navbar-container">
      <Menubar model={items} />
    </div>
  );
}
export default NavbarNew;
