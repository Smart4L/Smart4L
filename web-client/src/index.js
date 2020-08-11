import React from 'react';
import ReactDOM from 'react-dom';
import moment from 'moment';
import 'moment/locale/fr';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

moment.locale('fr');

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
