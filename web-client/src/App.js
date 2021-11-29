import React from 'react';
import { HashRouter as Router, Switch, Route} from 'react-router-dom';
import './assets/sass/main.scss'
import { Main } from './components/main/Main';
import Navbar from './components/navbar/Navbar';
import Radar from './components/radar/Radar';
import {Video} from './components/video/Video';
import {Settings} from './components/settings/Settings';

function App() {
  return (
    <Router>
      <Main/>
      <Navbar/>
    </Router>
  );
}

export default App;
