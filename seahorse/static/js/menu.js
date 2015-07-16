var Menu = React.createClass({displayName: 'Menu',
  render: function() {
    return (
      React.createElement("p", null, 
        React.createElement("a", {href: "/change/password/"}, "change password"), 
        " ", 
        React.createElement("a", {href: "/logout/"}, "logout")
      )
    );
  }
});


React.render(
  React.createElement(Menu, null),
  document.getElementById('menu')
);
