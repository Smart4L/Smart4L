import React from 'react';
import { HashRouter as Router, Switch, Route} from 'react-router-dom';
import './assets/sass/main.scss'
import Home from './components/home/Home';
import Navbar from './components/navbar/Navbar';
import Radar from './components/radar/Radar';
import {Video} from './components/video/Video';
import {Settings} from './components/settings/Settings';

function App() {
  return (
   <Router>
     <Switch>
       <Route exact path="/" component={Home}/>
       <Route exact path="/radar" component={Radar}/>
       <Route exact path="/video" component={Video}/>
       <Route exact path="/settings" component={Settings}/>
     </Switch>
     <Navbar/>
   </Router>
  );
}

export default App;
