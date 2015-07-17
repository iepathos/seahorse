

// TODO: Replace lame HelloWorld react app with something better

var HelloWorld = React.createClass({
  render: function() {
    return (
      <div>
        <h1>Seahorse Landing</h1>
        Hello, World!
        <br/>
        It is {this.props.date.toTimeString()}
      </div>
    );
  }
});

setInterval(function() {
  React.render(
    <HelloWorld date={new Date()} />,
    document.getElementById('content')
  );
}, 500);
