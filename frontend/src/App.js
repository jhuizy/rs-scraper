import React, { useState, useEffect } from 'react';
import './App.css';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

const loadSuggestions = (onLoaded) => {
  fetch("http://ge-tracker.jhuizy.com:3000/items/names")
    .then(res => res.json())
    .then(res => onLoaded(res.map(label => ({ label }))))
    .catch(console.err);
}

const loadItemHistory = (item, onLoaded) => {
  fetch(`http://ge-tracker.jhuizy.com:3000/items/${item}/history?page=0&per_page=200`)
    .then(res => res.json())
    .then(onLoaded)
    .catch(console.err);
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
      <Tooltip />
    </LineChart>
  )
}

export default (props) => {
  const [suggestions, setSuggestions] = useState(null)
  const [item, setItem] = useState("Magic logs")
  const [data, setData] = useState(null)

  useEffect(() => {
    if (suggestions == null) {
      loadSuggestions(setSuggestions)
    }
  }, [suggestions])

  useEffect(() => {
    if (data == null && item != null) {
      loadItemHistory(item, setData)
    }
    
  }, [data, item])

  return (
    <div>
      <form>
        <label htmlFor="name">Name</label>
        <input type="text" id="name" onChange={(e) => setItem(e.target.value)} value={item} />
        <input type="button" value="Search..." onClick={(e) => loadItemHistory(item, setData)} />
      </form>

      {data && renderData(data)}
    </div>
  );
}

