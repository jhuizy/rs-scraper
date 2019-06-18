import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

import { Container, Form, Icon, Input, Label } from 'semantic-ui-react'

const loadSuggestions = (onLoaded) => {
  fetch("http://ge-tracker.jhuizy.com:3000/items/names")
    .then(res => res.json())
    .then(res => onLoaded)
    .catch(console.err);
}

const loadItemHistory = (setLoading, item, onLoaded) => {
  setLoading(true);
  fetch(`http://ge-tracker.jhuizy.com:3000/items/${item}/history?page=0&per_page=200`)
    .then(res => res.json())
    .then(onLoaded)
    .catch(console.err)
    .finally(() => setLoading(false));
}

const renderData = (data) => {

  const amounts = data.map(x => x['overall_average']);
  const max = Math.max(...amounts)
  const min = Math.min(...amounts)

  const diff = max - min;
  const perc = diff * 0.1;
  const domain = [
    Math.floor(min - perc),
    Math.ceil(max + perc)
  ]

  return (
    <LineChart
      width={1000}
      height={300}
      data={data.slice(0, 50)}>
      <Line type="monotone" dataKey="overall_average" stroke="#8884d8" />
      <Line type="monotone" dataKey="sell_average" stroke="red" />
      <Line type="monotone" dataKey="buy_average" stroke="green" />
      <XAxis dataKey="time" />
      <YAxis domain={domain} />
      <CartesianGrid strokeOpacity={0.5} />
      <Tooltip />
    </LineChart>
  )
}

const renderSuggestion = (suggestion) => (
  <option value={suggestion} />
)

export default (props) => {
  const [suggestions, setSuggestions] = useState(null)
  const [item, setItem] = useState("Magic logs")
  const [data, setData] = useState(null)
  const [isLoading, setLoading] = useState(false)

  useEffect(() => {
    if (suggestions == null) {
      loadSuggestions(setSuggestions)
    }
  }, [suggestions])

  useEffect(() => {
    if (data == null && item != null) {
      console.log('')
      loadItemHistory(setLoading, item, setData)
    }

  }, [data, item])

  return (
    <div>
      <Container text style={{ margin: "20px" }}>
        <Form loading={isLoading}>
          <Form.Field>
            <label for="item-search">Item Name</label>
            <Input
              id="item-search"
              placeholder='eg. Magic logs'
              icon={<Icon name='search' inverted circular link />}
              onClick={(e) => loadItemHistory(setLoading, item, setData)}
              onChange={(e) => setItem(e.target.value)} value={item}
            />
            <datalist id='items'>
              {suggestions && suggestions.map(renderSuggestion)}
            </datalist>
          </Form.Field>
        </Form>
      </Container>
      {data && renderData(data)}
    </div>
  );
}

