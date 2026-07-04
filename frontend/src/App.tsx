import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/dashboard";
import Portfolio from "./pages/enter_portfolio";

function App() {

  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Dashboard />} />

        <Route path="/portfolio" element={<Portfolio />} />

      </Routes>

    </BrowserRouter>
  );

}

export default App;

