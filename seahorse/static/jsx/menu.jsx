var Menu = React.createClass({
  render: function() {
    return (
      <p>
        <a href="/change/password/">change password</a>
        &nbsp;
        <a href="/logout/">logout</a>
      </p>
    );
  }
});


React.render(
  <Menu />,
  document.getElementById('menu')
);
