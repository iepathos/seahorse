

// TODO: Replace lame HelloWorld react app with something better

var HelloWorld = React.createClass({displayName: 'HelloWorld',
  render: function() {
    return (
      React.createElement("div", null, 
        React.createElement("h1", null, "Seahorse Landing"), 
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
