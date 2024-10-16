import "./App.css";
import "./styles/util.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import {
  EventGeneralStats,
  EventNew,
  EventStats,
  Events,
  EventsListTest,
  EventsNew,
  MyEventsNew,
} from "./pages/Events";
import { Event } from "./pages/Events";
import { MyEvents } from "./pages/Events";
import { CreateEvent, CreateEventNew } from "./pages/CreateEvent";
import { Profile } from "./pages/Profile";
import { DataCollection } from "./pages/DataCollection";

import { PrimeReactProvider } from "primereact/api";
import "primereact/resources/primereact.min.css"; //core css
import "primeicons/primeicons.css"; //icons
import "primereact/resources/themes/lara-light-amber/theme.css";

function App() {
  return (
    <div className="App">
      <PrimeReactProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/events" element={<EventsListTest />} />
            <Route path="/events-new" element={<EventsNew />} />
            <Route path="/events/:id" element={<Event />}></Route>
            <Route path="/event-new/:id" element={<EventNew />} />
            <Route path="/signed" element={<div>signed</div>}></Route>
            <Route path="/created" element={<MyEvents />}></Route>
            <Route path="/created-new" element={<MyEventsNew />}></Route>
            <Route path="/new-event" element={<CreateEvent />} />
            <Route path="/new-event-new" element={<CreateEventNew />} />
            <Route path="/me" element={<Profile />} />
            <Route path="/data/:event_id" element={<DataCollection />} />
            <Route path="/general-stats" element={<EventGeneralStats />} />
            <Route path="/stats/:event_id" element={<EventStats />} />
            <Route path="*" element={<h1>Not Found</h1>} />
            <Route path="/test" element={<EventsListTest />} />
          </Routes>
        </BrowserRouter>
        <ToastContainer />
      </PrimeReactProvider>
    </div>
  );
}

export default App;
