// import React from 'react';
// import deburr from 'lodash/deburr';
// import Autosuggest from 'react-autosuggest';
// import match from 'autosuggest-highlight/match';
// import parse from 'autosuggest-highlight/parse';
// import TextField from '@material-ui/core/TextField';
// import Paper from '@material-ui/core/Paper';
// import MenuItem from '@material-ui/core/MenuItem';
// import Popper from '@material-ui/core/Popper';
// import { makeStyles } from '@material-ui/core/styles';

// function renderInputComponent(inputProps) {
//   const { classes, inputRef = () => { }, ref, ...other } = inputProps;

//   return (
//     <TextField
//       fullWidth
//       InputProps={{
//         inputRef: node => {
//           ref(node);
//           inputRef(node);
//         },
//         classes: {
//           input: classes.input,
//         },
//       }}
//       {...other}
//     />
//   );
// }

// function renderSuggestion(suggestion, { query, isHighlighted }) {
//   const matches = match(suggestion.label, query);
//   const parts = parse(suggestion.label, matches);

//   return (
//     <MenuItem selected={isHighlighted} component="div">
//       <div>
//         {parts.map(part => (
//           <span key={part.text} style={{ fontWeight: part.highlight ? 500 : 400 }}>
//             {part.text}
//           </span>
//         ))}
//       </div>
//     </MenuItem>
//   );
// }

// function getSuggestions(suggestions, value) {
//   const inputValue = deburr(value.trim()).toLowerCase();
//   const inputLength = inputValue.length;
//   let count = 0;

//   return inputLength === 0
//     ? []
//     : suggestions.filter(suggestion => {
//       const keep =
//         count < 5 && suggestion.label.slice(0, inputLength).toLowerCase() === inputValue;

//       if (keep) {
//         count += 1;
//       }

//       return keep;
//     });
// }

// function getSuggestionValue(suggestion) {
//   return suggestion.label;
// }

// const useStyles = makeStyles(theme => ({
//   root: {
//     height: 250,
//     flexGrow: 1,
//   },
//   container: {
//     position: 'relative',
//   },
//   suggestionsContainerOpen: {
//     position: 'absolute',
//     zIndex: 1,
//     marginTop: theme.spacing(1),
//     left: 0,
//     right: 0,
//   },
//   suggestion: {
//     display: 'block',
//   },
//   suggestionsList: {
//     margin: 0,
//     padding: 0,
//     listStyleType: 'none',
//   },
//   divider: {
//     height: theme.spacing(2),
//   },
// }));

// export default function IntegrationAutosuggest(props) {

//   const classes = useStyles();
//   const [anchorEl, setAnchorEl] = React.useState(null);
//   const [state, setState] = React.useState({
//     single: '',
//     popper: ''
//   });

//   const [stateSuggestions, setSuggestions] = React.useState([]);

//   const handleSuggestionsFetchRequested = ({ value }) => {
//     setSuggestions(getSuggestions(props.suggestions, value));
//   };

//   const handleSuggestionsClearRequested = () => {
//     setSuggestions([]);
//   };

//   const handleChange = name => (event, { newValue }) => {
//     if(this.props.handleChange) {
//       this.props.handleChange(newValue)
//     }
//     setState({
//       ...state,
//       [name]: newValue,
//     });
//   };

//   const autosuggestProps = {
//     renderInputComponent,
//     suggestions: stateSuggestions,
//     onSuggestionsFetchRequested: handleSuggestionsFetchRequested,
//     onSuggestionsClearRequested: handleSuggestionsClearRequested,
//     getSuggestionValue,
//     renderSuggestion,
//   };

//   return (
//     <div className={classes.root}>
//       <Autosuggest
//         {...autosuggestProps}
//         inputProps={{
//           classes,
//           id: 'react-autosuggest-simple',
//           label: 'Country',
//           placeholder: 'Search a country (start with a)',
//           value: state.single,
//           onChange: handleChange('single'),
//         }}
//         theme={{
//           container: classes.container,
//           suggestionsContainerOpen: classes.suggestionsContainerOpen,
//           suggestionsList: classes.suggestionsList,
//           suggestion: classes.suggestion,
//         }}
//         renderSuggestionsContainer={options => (
//           <Paper {...options.containerProps} square>
//             {options.children}
//           </Paper>
//         )}
//       />
//     </div>
//   );
// }
