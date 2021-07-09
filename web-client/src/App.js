import React from 'react';
import { HashRouter as Router } from "react-router-dom";

import './assets/sass/main.scss'
import { Main } from './components/main/Main';
import Navbar from './components/navbar/Navbar';

function App() {
  return (
    <Router>
      <Main/>
      <Navbar/>
    </Router>
  );
}

export default App;
