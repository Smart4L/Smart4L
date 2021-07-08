import React from 'react';
import { HashRouter as Router, Switch, Route} from 'react-router-dom';
import './assets/sass/main.scss'
import Home from './components/home/Home';
import Navbar from './components/navbar/Navbar';
import Radar from './components/radar/Radar';


function App() {
  return (
   <Router>
     <Switch>
       <Route exact path="/" component={Home}/>
       <Route exact path="/radar" component={Radar}/>
     </Switch>
     <Navbar/>
   </Router>
  );
}

export default App;
