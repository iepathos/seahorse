
var LandingMessage = React.createClass({
  render: function() {
    return (
      <div>
        <h1>Welcome to ehab.it</h1>
        <p>Ehab.it is a realtime, permission controlled action list with the ability
        to generate actions from emails and visa versa.  Ehab.it is invite only.</p>
      </div>
    );
  }
});


React.render(
  <LandingMessage />,
  document.getElementById('content')
);

