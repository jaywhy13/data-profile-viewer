import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import TableList from './components/TableList';
import TableDetail from './components/TableDetail';

class App extends Component {

  render() {
    return (
      <Router>
        <div>
          <Route exact path="/" component={TableList} />
          <Route path="/:table" component={TableDetail} />
        </div>
      </Router>
    );
  }
}

export default App;
