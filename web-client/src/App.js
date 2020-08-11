import React from 'react';
import './assets/sass/main.scss'
import Home from './components/home/Home';
import Navbar from './components/navbar/Navbar';

function App() {
  return (
    <React.Fragment>
      <Home/>
      <Navbar/>
    </React.Fragment>
  );
}

export default App;
