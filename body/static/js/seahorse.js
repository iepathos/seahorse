var HelloWorld = React.createClass({displayName: 'HelloWorld',
  render: function() {
    return (
      React.createElement("p", null, 
        "Hello, World!", 
        React.createElement("br", null), 
        "It is ", this.props.date.toTimeString()
      )
    );
  }
});

setInterval(function() {
  React.render(
    React.createElement(HelloWorld, {date: new Date()}),
    document.getElementById('content')
  );
}, 500);