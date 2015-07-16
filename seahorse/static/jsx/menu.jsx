var Menu = React.createClass({
  render: function() {
    return (
      <p>
        <a href="/logout/" class='pull-right'>logout</a>
      </p>
    );
  }
});


React.render(
  <Menu />,
  document.getElementById('menu')
);
