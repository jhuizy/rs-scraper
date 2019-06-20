import React from 'react'
import { Icon, Label, Menu, Table, Dimmer, Loader } from 'semantic-ui-react'

const loadItems = (onLoaded) => {
  fetch("http://ge-tracker.jhuizy.com:3001/unicorns")
    .then(res => res.json())
    .then(onLoaded)
    .catch(console.err);
}

const formatMoney = (gp) => {
  const rounded = () => {
    const M_10 = 10000000
    const K_10 = 10000
    if (gp > M_10) {
      return `${(gp / M_10).toFixed(2)}M`
    } else if (gp > K_10) {
      return `${(gp / K_10).toFixed(2)}K`
    } else {
      return gp
    }
  }

  return `${gp} (${rounded(gp)})`

}

const formatPercent = (perc) => {
  return perc.toFixed(2)
}

export default () => {

  const [items, setItems] = React.useState(null)
  const [loading, setLoading] = React.useState(false)

  React.useEffect(() => {
    setLoading(true)
    if (items == null) {
      loadItems(items => {
        setItems(items)
        setLoading(false)
      })
    }
  }, [items, loading])

  const renderRow = (item) => (
    <Table.Row>
      <Table.Cell>{item['name']}</Table.Cell>
      <Table.Cell>{formatMoney(item['buy'])}</Table.Cell>
      <Table.Cell>{formatMoney(item['sell'])}</Table.Cell>
      <Table.Cell>{formatPercent(item['margin_percent'])}</Table.Cell>
      <Table.Cell>{formatMoney(item['margin_gp'])}</Table.Cell>
      <Table.Cell>{item['score']}</Table.Cell>
    </Table.Row>
  )

  const renderTable = () => (
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

  const renderLoading = () => (
    <Dimmer active>
      <Loader>Loading</Loader>
    </Dimmer>
  )

  return (
    <div>
      {loading && renderLoading()}
      {!loading && renderTable()}
    </div>
  )
}
