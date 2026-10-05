import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import Portfolio from "./pages/enter_portfolio";
import Results from "./pages/results";
import Login from "./pages/login";
import Register from "./pages/register";
import ProtectedRoute from "./components/ProtectedRoute";
import Demo from "./pages/demo";
function App() {

  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/demo" element={<Demo />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/enter_portfolio" element={<Portfolio />} />
          <Route path="/results/:portfolioId" element={<Results />} />
        </Route>

      </Routes>

    </BrowserRouter>
  );

}

export default App;

