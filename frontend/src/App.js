import React from 'react';
import './App.css';
import Unicorns from './Unicorns'
import History from './History'
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { Container } from 'semantic-ui-react'

export default (props) => {
  return (
    <Router>
      <div>
        <Container>
          <Route path="/unicorns" component={Unicorns} />
          <Route path="/items" component={History} />
        </Container>
      </div>
    </Router>
  );
}

