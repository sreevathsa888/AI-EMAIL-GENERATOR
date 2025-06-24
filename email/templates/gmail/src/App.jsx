import { Routes, Route } from "react-router-dom";
import Landing from "./Landing";
import EmailApp from "./EmailApp";
import GeneratedEmail from "./GeneratedEmail";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/email" element={<EmailApp />} />
      <Route path="/generated-email" element={<GeneratedEmail />} />
    </Routes>
  );
}
