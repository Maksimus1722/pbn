jQuery(window).scroll(function () {
    "use strict";
  
    //sticky
    if (jQuery(this).scrollTop() > 50) {
      jQuery("header#theme-header").addClass("header-sticky");
    } else {
      jQuery("header#theme-header").removeClass("header-sticky");
    }
  });
  
  (function ($) {
    "use strict";
  
    var windowWidth = $(window).width();
  
    var loaded = false;
  
    //mobile
    function mobile_menu_offset(windowWidth) {
      if (windowWidth < 1024) {
        var mobile_menu_offset = $("#theme-header").outerHeight(true) - 10;
        $("nav.nav").css("top", mobile_menu_offset + "px");
      }
    }
  
    if (windowWidth < 1024) {
      $("header#theme-header nav a").on("click", function (event) {
        var submenu = $(" > .sub-menu", $(this).parent());
  
        if (submenu.length) {
          event.preventDefault();
  
          var this_opened_menu = $(this).closest(".menu > li");
          $("header#theme-header .menu > li")
            .not(this_opened_menu)
            .each(function () {
              $(".sub-menu", this).removeClass("open-menu");
            });
  
          submenu.toggleClass("open-menu");
          $(" > svg", $(this)).toggleClass("rotate");
        }
      });
    }
  
    $(".mobile-trigger").on("click", function (event) {
      event.preventDefault();
  
      $(this).toggleClass("is-active");
      $("header#theme-header nav").toggleClass("open");
      if ($(this).hasClass("is-active")) {
        $(".overlay").addClass("visible");
      } else {
        $(".overlay").removeClass("visible");
      }
    });
  
    function resize_tweaks(windowWidth) {
      if (windowWidth < 1024) {
        $("header#theme-header nav").removeClass("open");
        $("header#theme-header nav ul").removeClass("open-menu");
        $("header#theme-header .menu svg").removeClass("rotate");
  
        $(".mobile-trigger").removeClass("is-active");
      }
    }
  
    function close_overlay(windowWidth) {
      $(document).on("click", function (e) {
        if (
          $(e.target).closest(".mobile-trigger").length === 0 &&
          $(e.target).closest("header#theme-header nav").length === 0
        ) {
          $(".overlay").removeClass("visible");
  
          if (windowWidth < 1024) {
            //mobile menu
            $("header#theme-header nav").removeClass("open");
            $("header#theme-header nav ul").removeClass("open-menu");
            $(".mobile-trigger").removeClass("is-active");
          }
        }
      });
    }
  
    mobile_menu_offset(windowWidth);
  
    close_overlay(windowWidth);
  
    $(window).on("resize", function () {
      var windowWidth = $(window).width();
      resize_tweaks(windowWidth);
      close_overlay(windowWidth);
      mobile_menu_offset(windowWidth);
    });
  })(jQuery);
  
  (function ($) {
  
    $(document).on("keydown", function (event) {
      if (event.key == "Escape") {
        $(".overlay").removeClass("visible");
        $("nav#primary").removeClass("open");
        $(".mobile-trigger").removeClass("is-active");
      }
    });
  })(jQuery);
  jQuery(document).ready(function($) {
      $(".primary .menu").addClass("responsive-menu");
      $(window).resize(function(){
          if(window.innerWidth > 1024) {
              $(".primary .menu, nav .sub-menu, nav .children").removeAttr("style");
              $(".responsive-menu > li").removeClass("menu-open");
          }
      });
  
      $(".responsive-menu > li").click(function(event){
          if (event.target !== this)
          return;
          $(this).find(".sub-menu:first").toggleClass('submenu-toggle').parent().toggleClass("menu-open");
          $(this).find(".children:first").toggleClass('submenu-toggle').parent().toggleClass("menu-open");
      });
  
      $("div.responsive-menu > ul > li").click(function(event) {
          if (event.target !== this)
              return;
          $(this).find("ul:first").toggleClass('submenu-toggle').parent().toggleClass("menu-open");
      });
  
  });