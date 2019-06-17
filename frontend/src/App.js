import React from 'react';
import './App.css';
import Unicorns from './Unicorns'
import History from './History'

import { Container } from 'semantic-ui-react'

export default (props) => {
  return (
    <div>
      <Container>
        <Unicorns />
        <History />
      </Container>
    </div>
  );
}

