var Menu = React.createClass({
  render: function() {
    return (
      <a href="/logout/" class='pull-right'>logout</a>
    );
  }
});

setInterval(function() {
  React.render(
    <Menu />,
    document.getElementById('menu')
  );
}, 500);