
var LandingMessage = React.createClass({displayName: 'LandingMessage',
  render: function() {
    return (
      React.createElement("div", null, 
        React.createElement("h1", null, "Welcome to ehab.it"), 
        React.createElement("p", null, "Ehab.it is a realtime, permission controlled action list with the ability" + ' ' +
        "to generate actions from emails and visa versa.  Ehab.it is invite only.")
      )
    );
  }
});


React.render(
  React.createElement(LandingMessage, null),
  document.getElementById('content')
);

