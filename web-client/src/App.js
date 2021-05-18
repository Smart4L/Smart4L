import React from 'react';
import { HashRouter as Router, Switch, Route, withRouter } from "react-router-dom";
import './assets/sass/main.scss'
import Home from './components/home/Home';
import Navbar from './components/navbar/Navbar';
import Stats from './components/stats/Stats';
import Map from './components/map/Map';
import Settings from './components/settings/Settings';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/stats" component={withRouter(Stats)}/>
        <Route exact path="/map" component={withRouter(Map)}/>
        <Route exact path="/settings" component={withRouter(Settings)}/>
        <Route exact path="/" component={withRouter(Home)}/>
      </Switch>
      <Navbar/>
    </Router>
  );
}

export default App;
