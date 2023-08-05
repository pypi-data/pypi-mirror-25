$( document ).ready(function() {
  // Replace any fa-icon roles
  $('.fa-icon').each(function(){$(this).html('<i class="fa ' + $(this).html() + '" aria-hidden="true"></i>')})
  // Temp index fix
  $('a').each( function(a) {
    var minusIndex = this.href.replace(/index.html/i, '')
    $(this).attr('href', minusIndex)
  })
  // Move current guide to top of TOC
  $('#globaltoc').prepend($('ul').has('.toctree-l1.current'))
  // Lightbox
  // Show proper cursor only if img
  $('.reference.internal').has("img").hover(function(){
    $(this).css("cursor", "zoom-in")
  });
  // Open Lightbox
  $('.reference.internal').has("img").on('click', function(e) {
    e.preventDefault();
    var image = $(this).attr('href');
    $('html').addClass('no-scroll');
    $('body').append('<div class="lightbox-opened"><img src="' + image + '"></div>');
  });

  // Close Lightbox
    $('body').on('click', '.lightbox-opened', function() {
    $('html').removeClass('no-scroll');
    $('.lightbox-opened').remove();
  });
  // Apply affix if window tall enough
  function checkSizeAffix() {
    if ($('#main > .section').height() >= 700) {
      $('.version-and-toc').affix({
        offset: {
          top: 128,
          bottom: 368
        }
      })
    }
    if ($('#main > .section').height() <= 699) {
      $(window).off('.affix')
      $('.version-and-toc').removeData('bs.affix').removeClass('affix affix-top affix-bottom')
    }
  }
  checkSizeAffix();
  //$(window).resize(checkSizeAffix())

  //Quick find
   $('#main').click(function() {
    if ($('#quickfind').val().length == 0) {
      $('#globaltoc').children('ul').not('.current').hide()
      $("[class^='toctree']").not('.current').children('.toc-collapsible-btn').each(function() {
        tocTarget = this;
        tocCollapse();})
      }
    }
  )
  ////////////////
  // Mobile TOC//
  ///////////////

  // Mobile global TOC
  $('<div class="g-menu-btn" id="g-menu-btn"><i id="g-closedMenu" class="fa fa-bars" aria-hidden="true"></i><i id="g-openMenu" class="fa fa-times" aria-hidden="true" style="display: none;"></i>   </div>').insertAfter('.toctree-l1.current>a')
  function expandGlobalTOC() {
    $('.g-menu-btn').siblings('ul').addClass('expand');
    $('.g-menu-btn').siblings('ul').slideToggle(300)
    $('#g-closedMenu').hide()
    $('#g-openMenu').show()
  }
  function collapseGlobalTOC() {
    $('.g-menu-btn').siblings('ul').removeClass('expand');
    $('.g-menu-btn').siblings('ul').slideToggle(300)
    $('#g-closedMenu').show()
    $('#g-openMenu').hide()
  }
  // $(window).resize(function() {
  // if ($(window).width() > 864) {
  //   $('.toc').find('*').not('#g-openMenu', '#g-closedMenu').removeAttr( 'style' );
  //   }
  // })
  $('.g-menu-btn').click(function(){
    if ($('.g-menu-btn').siblings('ul').hasClass('expand')){
        collapseGlobalTOC();
      } else {
        expandGlobalTOC();
      }
    })
  // Mobile local TOC
  $('#menu').children().slideToggle(0);
  $('#openMenu').hide()
  $('.menu-btn').click(function(){
    if ($('#menu').hasClass('expand')){
          $('#menu').removeClass('expand');
          $('#menu').children().slideToggle(300);
          $('#closedMenu').show()
          $('#openMenu').hide()
                        } else {
          $('#menu').addClass('expand');
          $('#menu').children().slideToggle(300);
          $('#closedMenu').hide()
          $('#openMenu').show()
        }
      })
  // Hide empty TOCs on desktop
  if ($('ul.current > li > ul').children().length == 0) {
    $('ul.current > li > ul').hide();
  }
  // Hide empty mobile global TOC if no children
  if ($('ul.current').children().length == 0){
    $('.g-menu-btn').hide();
  }
  // Hide empty mobile slider menus
  if ($('#menu > ul > li').children().length == 1) {
    $('#menu > ul > li').hide();
    $('#menu-btn').hide();
  }

  // Constructors
  $('.property').siblings('.descclassname').show()
  $('.property').hide()

  /////////////////////////
  // Expandable sections //
  /////////////////////////

  // Check for collapsible signaler
  $(':header:contains("[[]]")').html(function (i, t) {
    $(this).addClass('collapsible');
    return t.replace('[[]]', '<span class="hidden"> </span>');
  })
  $('.collapsible').addClass('collapsed');
  $('.collapsible').attr('aria-expanded','false')
  $('.collapsible').siblings().slideToggle(0);
  // Remove signaler from references—toc and in main
  $('.reference:contains("[[]]")').html(function (i, t) {
    return t.replace('[[]]', '<span class="hidden"> </span>');
  })

  // Make it clickable
  $('.collapsible').click( function() {
    if ($(this).hasClass('collapsed')){
      $(this).removeClass('collapsed');
      $(this).attr('aria-expanded','true')
      $(this).siblings().slideToggle(300);
      $("span[id]").attr('style','display: none;')
      $(this).siblings().not('span').wrapAll('<div class="colsection"></div>');
      $(this).after($(this).siblings(".colsection"));
    } else {
      $(this).addClass('collapsed');
      $(this).attr('aria-expanded','false')
      $(this).siblings('.colsection').children().slideToggle(300);
      $("span[id]").attr('style','display: none;')
      $(this).siblings('.colsection').children().unwrap();
    }
  });
  // Keyboard navigation for collapsible sections
  $(".collapsible").attr("tabindex", "0");
  $(".collapsible").on("keydown", function(e){
    if(e.which === 13){
      $(this).trigger("click");
    }
  });
  // Unhide section if user is referred its anchor
  function unhideCollapsed()
  {
    try {
    var anchorName = document.location.hash.substring(1);
    var collapsedAnchor = $("[id=" + anchorName + "]").children(".collapsed");
    $(collapsedAnchor).removeClass('collapsed');
    $(collapsedAnchor).attr('aria-expanded','true');
    $(collapsedAnchor).siblings().slideToggle(300);
    $("span[id]").attr('style','display: none;');
    $(collapsedAnchor).siblings().wrapAll('<div class="colsection"></div>');
    $(collapsedAnchor).after($(collapsedAnchor).siblings(".colsection"));
    } catch (e) {}
    try {
      var anchorName = document.location.hash.substring(1);
      var collapsedAnchor = $("[id=" + anchorName + "]").siblings(".collapsed");
      $(collapsedAnchor).removeClass('collapsed');
      $(collapsedAnchor).attr('aria-expanded','true');
      $(collapsedAnchor).siblings().slideToggle(300);
      $("span[id]").attr('style','display: none;');
      $(collapsedAnchor).siblings().wrapAll('<div class="colsection"></div>');
      $(collapsedAnchor).after($(collapsedAnchor).siblings(".colsection"));
    } catch (e) {}
  }
  unhideCollapsed();
  // Unhide section if user changes hash in page
  $(window).on('hashchange', function(e){
   unhideCollapsed();
  });

  //////////////////////////
  // Guides dropdown menu //
  //////////////////////////

  $(".nav-dropdown").on("keydown", function(e){
    if(e.which === 13){
      $(this).toggleClass("showdrop");
      $('.nav-sub-menu').attr("aria-hidden", function(index, attr) {return attr == "true" ? "false" : "true"});
      $('.nav-sub-menu', this).toggle();
    }
  });
  // Guides dropdown
  $("li.nav-dropdown").hover(function() {
    $(this).addClass("showdrop")
    $('.nav-sub-menu').attr("aria-hidden", "false")
    $(".nav-sub-menu").show();
  }, function() {
    $('.nav-sub-menu').attr("aria-hidden", "true")
    $(this).removeClass("showdrop");
    $(".nav-sub-menu").hide()
  });
  // toc Nav
  function tocCollapse() {
    $(tocTarget).addClass('collapsed');
    $(tocTarget).attr('aria-expanded','false')
    $(tocTarget).siblings('ul').slideUp(slideTime);
  }
  function tocOpen() {
    $(tocTarget).removeClass('collapsed');
    $(tocTarget).attr('aria-expanded','true')
    $(tocTarget).siblings('ul').slideDown(slideTime);
  }
  $("[class^='toctree']").has('ul').prepend("<button class=\"toc-collapsible-btn collapsible collapsed\" type=\"button\"></button>")
  slideTime = 0
  tocTarget = "#globaltoc .toc-collapsible-btn"
  tocCollapse()
  tocTarget = "#globaltoc .current > .toc-collapsible-btn"
  tocOpen()
  slideTime = 200
  $('.toc-collapsible-btn').click(function() {
    tocTarget = this
    if ($(this).hasClass('collapsed') == true) {
      tocOpen();
    } else {
      tocCollapse();
    }
  })
  // TOC button color set
  $("[class^='toctree']").each(function() {
    if ($(this).css('background-color') == "rgb(255, 255, 255)") {
      $(this).find('.toc-collapsible-btn').css('color','#098297')}
  })
  // Quick find
  $('#quickfind').click(function() {
     if ($('#quickfind').val().length == 0) {
      $(".toctree-l1 > a").css('display','inline-block');
      $('#globaltoc').find('*').not('.g-menu-btn').not('.toc-collapsible-btn').not('#g-closedMenu').not('#g-openMenu').show();
      $('.toctree-l1').css('display','flex');
      $('.toc-collapsible-btn').each(function () {
        tocTarget = this;
        tocOpen();
      })
    }
  })
  $('#quickfind').keydown(function() {
    $('.toc-collapsible-btn').each(function () { // Reopen collapsed sections so user understands why searches appear within them
        tocTarget = this;
        slideTime = 0;
        tocOpen();
        slideTime = 200;
      })
  })
  $('#quickfind').keyup(function() {
    var findFor = this.value.toLowerCase();
    $('#globaltoc .reference').each(function() {
      var itemLC = $(this).text().toLowerCase();
      (itemLC.indexOf(findFor) > -1) ? $(this).parents().show() : $(this).parent().hide();
    })
  })
})
// Additional functions
function expandAll (){
  $('.collapsible').siblings('.colsection').children().unwrap();
  $('.collapsible').siblings().slideDown(300);
  $('.collapsible').removeClass('collapsed');
  $('.collapsible').attr('aria-expanded','true')
  $('.collapsible').each(function addColSecAll(){$(this).siblings().wrapAll('<div class="colsection"></div>')});
}
function collapseAll (){
  $('.collapsible').siblings('.colsection').children().slideToggle(300);
  $("span[id]").attr('style','display: none;')
  $('.collapsible').siblings('.colsection').children().unwrap();
  $('.collapsible').addClass('collapsed');
  $('.collapsible').attr('aria-expanded','false')
}
function versionPick(p1){
  var clickedVer = p1.textContent;
  var hostAndVer = "docs.skuid.com\/"
  var fullURL = hostAndVer.concat(clickedVer,"\/")
  var siteVer = new RegExp("docs.skuid.com\/[^\/]+\/")
  window.location.href = document.location.href.replace(siteVer, fullURL)
}