var Menu = React.createClass({displayName: 'Menu',
  render: function() {
    return (
      React.createElement("a", {href: "/logout/", class: "pull-right"}, "logout")
    );
  }
});

setInterval(function() {
  React.render(
    React.createElement(Menu, null),
    document.getElementById('menu')
  );
}, 500);