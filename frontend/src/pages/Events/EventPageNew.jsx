import EventDetail from "../../components/Events/EventDetail";
import NavbarNew from "../../components/NavbarNew";
import NavbarTest from "../../components/NavbarTest";

function EventPageNew() {
  return (
    <>
      <NavbarTest />
      <div className="flex justify-center items-center max-h-screen mt-24">
        <EventDetail />
      </div>
    </>
  );
}
export default EventPageNew;
