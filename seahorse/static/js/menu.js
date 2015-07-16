var Menu = React.createClass({displayName: 'Menu',
  render: function() {
    return (
      React.createElement("p", null, 
        React.createElement("a", {href: "/logout/", class: "pull-right"}, "logout")
      )
    );
  }
});


React.render(
  React.createElement(Menu, null),
  document.getElementById('menu')
);
