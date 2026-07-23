import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/dashboard";
import Portfolio from "./pages/enter_portfolio";
import Results from "./pages/results";

function App() {

  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Dashboard />} />

        <Route path="/enter_portfolio" element={<Portfolio />} />

        <Route path="/results/:portfolioId" element={<Results />} />
      </Routes>

    </BrowserRouter>
  );

}

export default App;

