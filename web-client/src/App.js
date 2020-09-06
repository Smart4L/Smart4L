import React from 'react';
import { HashRouter as Router, Switch, Route, withRouter } from "react-router-dom";
import './assets/sass/main.scss'
import Home from './components/home/Home';
import Navbar from './components/navbar/Navbar';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={withRouter(Home)}/>
      </Switch>
      <Navbar/>
    </Router>
  );
}

export default App;
