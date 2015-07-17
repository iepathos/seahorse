
function isLoggedIn(){
  // checks if userCookie is set, no need to validate cookie,
  // this is just to determine menu state
  var userCookie = getCookie("user");
  if (userCookie != undefined) {
    return true;
  } else {
    return false;
  }
}

var HomeButton = React.createClass({displayName: 'HomeButton',
  render: function() {
    return (
      React.createElement("a", {href: "/"}, "home")
    );
  }
});

var BlogButton = React.createClass({displayName: 'BlogButton',
  render: function() {
    return (
      React.createElement("a", {href: "/blog/"}, "blog")
    );
  }
});

var RegisterButton = React.createClass({displayName: 'RegisterButton',
  render: function() {
    return (
      React.createElement("a", {href: "/register/"}, "register")
    );
  }
});

var LoginButton = React.createClass({displayName: 'LoginButton',
  render: function() {
    return (
      React.createElement("a", {href: "/login/"}, "login")
    );
  }
});

var LogoutButton = React.createClass({displayName: 'LogoutButton',
  render: function() {
    return (
      React.createElement("a", {href: "/logout/"}, "logout")
    );
  }
});

var ChangePasswordButton = React.createClass({displayName: 'ChangePasswordButton',
  render: function() {
    return (
      React.createElement("a", {href: "/change/password/"}, "change password")
    );
  }
});

var ResetPasswordButton = React.createClass({displayName: 'ResetPasswordButton',
  render: function() {
    return (
      React.createElement("a", {href: "/reset/password/"}, "reset password")
    );
  }
});


menu_elements = [React.createElement(HomeButton, null), React.createElement(BlogButton, null)]

if (isLoggedIn()) {
  menu_elements.push(React.createElement(ChangePasswordButton, null), React.createElement(LogoutButton, null))
} else {
  menu_elements.push(React.createElement(RegisterButton, null), React.createElement(LoginButton, null))
}


var Menu = React.createClass({displayName: 'Menu',
  render: function() {
    return (
      React.createElement("div", {className: "nav"}, 
        React.createElement("ul", null, 
          menu_elements.map(function(link, i){
            return React.createElement("li", {key: i}, link)
          })
        )
      )
    );
  }
});

React.render(
  React.createElement(Menu, null),
  document.getElementById('menu')
);
