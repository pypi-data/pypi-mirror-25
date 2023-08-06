var userInfo = null;
var showConsole = null;
var roles = null;
var portal = null;
var portals = null;
var menus = [];
var tabs;
$(function () {
  // init tabs
  tabs = $$('#tabs').cleverTabs({
    setupContextMenu: false,
    lockOnlyOne: true,
  });

  // get data from superset
  var bootstrapData = JSON.parse($('#app').attr('data-bootstrap'));
  // console.info(bootstrapData);
  portal = bootstrapData.portal;
  portals = bootstrapData.portals;
  roles = bootstrapData.roles;
  showConsole = bootstrapData.showConsole;
  $('#profileName').html(bootstrapData.username);
  menus = bootstrapData.menus;
  init();

  // let array to parent-children data
  var nodes = getJsonMenu(0, menus);
  // set nav bar
  var html = setNavBar(nodes);
  $('#side-bar ul').first().append(html);

  $(".page-sidebar-menu >.nav-item > a").click(function () {
    $(".page-sidebar-menu > .nav-item > a").removeClass("click").addClass("unclick");
    $(this).removeClass("unclick").addClass("click");
    // $('#side-bar > ul > li .sub-menu').css('display', 'none');
    // $(this).next().css('display', 'block');

  });

});


function init() {
  // set portal info(logo, footer)
  $.get('/static/assets/resources/portalManage/logo/logo_' + portal[0] + '_' + portal[4] + '.png').success(function (data) {
    $('.page-logo img').attr('src', '/static/assets/resources/portalManage/logo/logo_' + portal[0] + '_' + portal[4] + '.png');
  }).error(function (xhr, error) {
    if (xhr.status === 404) {
      $('.page-logo img').attr('src', '/static/assets/resources/portalShow/logo.png');
    }
  })
  $('#footer').html(portal[5]);
  
  if (showConsole) {
    $('#console').show();
  }
  // show console
  // var roleArray = roles.substring(1, roles.length - 1).split(',');
  // for (var i = 0; i < roleArray.length; i++) {
  //   if (roleArray[i].trim() === 'Admin') {
  //     $('#console').show();
  //   }
  // }
  // switch portal
  var portalStr = '';
  portals.forEach(p => {
    if (p[0] === portal[0]) {
      portalStr += '<li><a href="javascript:;" style="background: #4297d7;"><i class="fa fa-home" style="color: white;"></i><span style="margin-left: 10px; color: white; font-size: 12px;">' + p[1] + '</span></a></li>';
    } else {
      portalStr += '<li><a href="/hand/portal/' + p[0] + '/show"><i class="fa fa-home"></i><span style="margin-left: 10px;  font-size: 12px;">' + p[1] + '</span></a></li>';
    }
  });
  $('#portal').html(portal[1]);
  $('#portals').html(portalStr);

  // set default dashboard
  menus.forEach(menu => {
    if (menu[5] === 'true') {
      tabs.add({
        url: '/superset/dashboard/' + menu[3] + '?standalone=true&isControl=false&isTitle=false&isManager=false',
        label: menu[1]
      });
      var tab = tabs.getTabByUrl('/superset/dashboard/' + menu[3] + '?standalone=true&isControl=false&isTitle=false&isManager=false');
      tab.setLock(true);
    }
  });

  // set autoComplete
  var parentIds = [];
  menus.forEach(menu => {
    if (menu[2] !== 0 && $.inArray(menu[2], menus) === -1) {
      parentIds.push(menu[2]);
    }
  })
  var availableDashboards = [];
  menus.forEach(menu => {
    if ($.inArray(menu[0], parentIds) === -1) {
      availableDashboards.push({
        label: menu[1],
        value: menu[1]
      });
    }
  })
  // set search autocomplete input
  $("#search").autocomplete({
    source: availableDashboards
  });

  // init portal theme
  $.get('/hand/portal/getTheme').done(function (data) {
    var result = JSON.parse(data);
    $("#" + result.color).addClass("current");

    $(".theme-panel .layout-style-option").val(result.themeStyle);
    $(".theme-panel .layout-option").val(result.layout);
    $(".theme-panel .page-header-option").val(result.header);
    $(".theme-panel .page-header-top-dropdown-style-option").val(result.top_menu);
    $(".theme-panel .sidebar-option").val(result.sidebar_mode);
    $(".theme-panel .sidebar-menu-option").val(result.sidebar_menu);
    $(".theme-panel .sidebar-style-option").val(result.sidebar_style);
    $(".theme-panel .sidebar-pos-option").val(result.sidebar_position);
    $(".theme-panel .page-footer-option").val(result.footer);

  }).fail(function (xhr, error) {
    alert('error')
  });

}

// open new iframe
function openFrame(name, href) {
  tabs.add({
    url: '/superset/dashboard/' + href + '?standalone=true&isControl=false&isTitle=false&isManager=false',
    label: name
  });
}

function query() {
  var flag = true;
  var dashboardName = $('#search').val();
  if (dashboardName === '') {
    return;
  }
  menus.forEach(menu => {
    if (dashboardName === menu[1]) {
      flag = false;
      $("#search").val("");
      openFrame(menu[1], menu[3]);
    }
  });
  if (flag) {
    alert('the dashboard does not exist');
  }
}


// let array to parent-children data
function getJsonMenu(id, menus) {
  if (id !== 0) {
    var children = [];
    for (var i = 0; i < menus.length; i++) {
      var menu = menus[i];
      if (menu[2] === id) {
        var node = {
          id: menu[0],
          name: menu[1],
          parent_id: menu[2],
          dashboard_href: menu[3],
          open_way: menu[4],
          is_index: menu[5],
          icon: menu[6],
        };
        node.children = getJsonMenu(menu[0], menus);
        children.push(node);
      }
    }
    return children;
  }
  // id == 0
  var nodes = [];
  for (var i = 0; i < menus.length; i++) {
    var menu = menus[i];
    if (menu[2] === 0) {
      var node = {
        id: menu[0],
        name: menu[1],
        parent_id: menu[2],
        dashboard_href: menu[3],
        open_way: menu[4],
        is_index: menu[5],
        icon: menu[6],
      };
      node.children = getJsonMenu(menu[0], menus);
      nodes.push(node);
    }
  }
  return nodes;
}

// set nav bar
function setNavBar(menuObj) {
  var vdom = [];
  if (menuObj instanceof Array) {
    var list = [];
    for (var item of menuObj) {
      list.push(setNavBar(item));
    }
    // console.info(list)
    vdom.push(
      list.join('')
    );
  } else {
    // set arrow
    var arrow = '';
    var aClick = '';
    if (menuObj.children.length > 0) {
      arrow = '<span class="arrow"></span>';
    }
    if (menuObj.children.length === 0) {
      aClick = ' onclick="openFrame(\'' + menuObj.name + '\', \'' + menuObj.dashboard_href + '\')" ';

    }
    if (menuObj.children.length > 0) {
      // have no child
      vdom.push(
        '<li class="nav-item " >' +
        '<a href="#"' + aClick + 'class="nav-link nav-toggle">' +
        '<i class="' + menuObj.icon + '"></i>' +
        '<span class="title" style="margin-left: 10px; font-size: 12px;">' + menuObj.name + '</span>' +
        arrow +
        '</a>' +
        '<ul class="sub-menu">' +
        setNavBar(menuObj.children) +
        '</ul>' +
        '</li>'
      );
    } else {
      vdom.push(
        '<li class="nav-item">' +
        '<a href="#"' + aClick + 'class="nav-link nav-toggle">' +
        '<i class="' + menuObj.icon + '"></i>' +
        '<span class="title" style="margin-left: 10px;font-size: 12px;">' + menuObj.name + '</span>' +
        arrow +
        '</a>' +
        setNavBar(menuObj.children) +
        '</li>'
      );
    }

  }
  return vdom.join('');
}

// update password
function updatePassword() {
  if ($('#newPassword').val().trim().length < 6) {
    $('#updatePasswordMsg').html('<div class="alert alert-warning"><strong>警告!</strong> 密码长度不少于6位. </div>');
    return;
  }
  if ($('#newPassword').val() !== $('#newPassword2').val()) {
    $('#updatePasswordMsg').html('<div class="alert alert-warning"><strong>警告!</strong> 两次密码输入不一致. </div>');
    return;
  }
  $.post('/hand/portal/updatePassword', { newPassword: $('#newPassword').val() }, function (data) {
    if (data === 'success') {
      $('#updatePasswordMsg').html('<div class="alert alert-success"> 密码修改成功. </div>');
      setTimeout(function () {
        $('#updatePasswordModal').modal('hide');
      }, 300);
    } else {
      $('#updatePasswordMsg').html('<div class="alert alert-danger"> 密码修改失败. </div>');
    }
  });

}

function opneUserInfoModal() {
  $.get('/hand/portal/getUserInfo', function (data) {
    userInfo = JSON.parse(data);
    // set user info
    $('#username').html(userInfo.username);
    $('#isActive').html(userInfo.active === true ? 'True' : 'False');
    $('#role').html(userInfo.roles);
    $('#loginCount').html(userInfo.login_count);
    $('#firstName').html(userInfo.first_name);
    $('#lastName').html(userInfo.last_name);
    $('#email').html(userInfo.email);
    $('#userInfoModal').modal('show');
  });
}

function openUpdateUserInfoModal() {
  $('#updateUserInfoMsg').html('');
  $('#firstName2').val(userInfo.first_name);
  $('#lastName2').val(userInfo.last_name);
  $('#email2').val(userInfo.email);
  $('#updateUserInfoModal').modal('show');
}

// return to userInfo
function returnUserInfo(model) {
  $('#' + model).modal('hide');
  $('#userInfoModal').modal('show');
}

// update user info
function updateUserInfo() {
  if ($('#firstName2').val().trim() === '' || $('#lastName2').val().trim() === '' || $('#email2').val().trim() === '') {
    $('#updateUserInfoMsg').html('<div class="alert alert-warning"><strong>警告!</strong> 修改的信息不能为空 </div>');
    return;
  }
  $.post('/hand/portal/updateUserInfo',
    { firstName: $('#firstName2').val(), lastName: $('#lastName2').val(), email: $('#email2').val() },
    function (data) {
      if (data === 'success') {
        $('#updateUserInfoMsg').html('<div class="alert alert-success"> 信息修改成功. </div>');
        setTimeout(function () {
          $('#updateUserInfoModal').modal('hide');
        }, 300);
      } else {
        $('#updateUserInfoMsg').html('<div class="alert alert-danger"> 信息修改失败. </div>');
      }
    });

}