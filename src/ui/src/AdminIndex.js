import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Admin from './Admin';
import * as serviceWorker from './serviceWorker';

/**
*   @author @MartinStanchev
*/
ReactDOM.render(<Admin />, document.getElementById('admin'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
