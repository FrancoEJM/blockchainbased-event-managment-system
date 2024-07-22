import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import {
  EventGeneralStats,
  EventStats,
  Events,
  EventsListTest,
} from "./pages/Events";
import { Event } from "./pages/Events";
import { MyEvents } from "./pages/Events";
import { CreateEvent } from "./pages/CreateEvent";
import { Profile } from "./pages/Profile";
import { DataCollection } from "./pages/DataCollection";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/events" element={<Events />} />
          <Route path="/events/:id" element={<Event />}></Route>
          <Route path="/signed" element={<div>signed</div>}></Route>
          <Route path="/created" element={<MyEvents />}></Route>
          <Route path="/new-event" element={<CreateEvent />} />
          <Route path="/me" element={<Profile />} />
          <Route path="/data/:event_id" element={<DataCollection />} />
          <Route path="/general-stats" element={<EventGeneralStats />} />
          <Route path="/stats/:event_id" element={<EventStats />} />
          <Route path="*" element={<h1>Not Found</h1>} />
          <Route path="/test" element={<EventsListTest />} />
        </Routes>
      </BrowserRouter>
      <ToastContainer />
    </div>
  );
}

export default App;
