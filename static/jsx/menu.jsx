
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

var HomeButton = React.createClass({
  render: function() {
    return (
      <a href="/">home</a>
    );
  }
});

var BlogButton = React.createClass({
  render: function() {
    return (
      <a href="/blog/">blog</a>
    );
  }
});

var RegisterButton = React.createClass({
  render: function() {
    return (
      <a href="/register/">register</a>
    );
  }
});

var LoginButton = React.createClass({
  render: function() {
    return (
      <a href="/login/">login</a>
    );
  }
});

var LogoutButton = React.createClass({
  render: function() {
    return (
      <a href="/logout/">logout</a>
    );
  }
});

var ChangePasswordButton = React.createClass({
  render: function() {
    return (
      <a href="/change/password/">change password</a>
    );
  }
});

var ResetPasswordButton = React.createClass({
  render: function() {
    return (
      <a href="/reset/password/">reset password</a>
    );
  }
});


menu_elements = [<HomeButton />, <BlogButton />]

if (isLoggedIn()) {
  menu_elements.push(<ChangePasswordButton />, <LogoutButton />)
} else {
  menu_elements.push(<RegisterButton />, <LoginButton />)
}


var Menu = React.createClass({
  render: function() {
    return (
      <div className="nav">
        <ul>
          {menu_elements.map(function(link, i){
            return <li key={i}>{link}</li>
          })}
        </ul>
      </div>
    );
  }
});

React.render(
  <Menu />,
  document.getElementById('menu')
);
