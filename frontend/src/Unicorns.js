import React from 'react'
import { Icon, Label, Menu, Table } from 'semantic-ui-react'

const loadItems = (onLoaded) => {
  fetch("http://ge-tracker.jhuizy.com:3001/unicorns")
    .then(res => res.json())
    .then(onLoaded)
    .catch(console.err);
}

export default () => {

  const [items, setItems] = React.useState(null)

  React.useEffect(() => {
    if (items == null) {
      loadItems(setItems)
    }
  }, [items])
  
  const renderRow = (item) => (
        <Table.Row>
          <Table.Cell>{item['name']}</Table.Cell>
          <Table.Cell>{item['buy']}</Table.Cell>
          <Table.Cell>{item['sell']}</Table.Cell>
          <Table.Cell>{item['margin_percent']}</Table.Cell>
          <Table.Cell>{item['margin_gp']}</Table.Cell>
          <Table.Cell>{item['score']}</Table.Cell>
        </Table.Row>
  )

  return (
    <Table celled>
      <Table.Header>
        <Table.Row>
          <Table.HeaderCell>Name</Table.HeaderCell>
          <Table.HeaderCell>Buy</Table.HeaderCell>
          <Table.HeaderCell>Sell</Table.HeaderCell>
          <Table.HeaderCell>Margin %</Table.HeaderCell>
          <Table.HeaderCell>Margin GP</Table.HeaderCell>
          <Table.HeaderCell>Score</Table.HeaderCell>
        </Table.Row>
      </Table.Header>

      <Table.Body>
        {items && items.map(renderRow)}
      </Table.Body>
    </Table>
  )
}
