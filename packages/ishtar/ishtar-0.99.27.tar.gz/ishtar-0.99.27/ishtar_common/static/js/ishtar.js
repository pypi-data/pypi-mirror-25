/* CSRFToken management */

$.ajaxSetup({
beforeSend: function(xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
}});

function manage_async_link(event){
    event.preventDefault();
    var url = $(this).attr('href');
    var target = $(this).attr('data-target');
    $.get(url, function(data) {
        $(target).html(data);
    });
}

/* default function to prevent undefined */
function get_next_table_id(){}
function get_previous_table_id(){}

var shortcut_url = '';
var advanced_menu = false;
var shortcut_menu_hide = false;
var activate_all_search_url = '/activate-all-search/';
var activate_own_search_url = '/activate-own-search/';
var activate_advanced_url = '/activate-advanced-menu/';
var activate_simple_url = '/activate-simple-menu/';
var shortcut_menu_hide_url = '/hide-shortcut-menu/'
var shortcut_menu_show_url = '/show-shortcut-menu/'

function init_shortcut_menu(html){
    $("#progress").hide();
    $("#context_menu").html(html);
    $(".chosen-select").chosen();
    if (advanced_menu) {
        init_advanced_shortcut_fields();
    } else {
        init_shortcut_fields();
    }
    $("#short-menu-advanced").click(function(){
        $.get(url_path + activate_advanced_url,
               load_shortcut_menu
        );
    });
    $("#short-menu-simple").click(function(){
        $.get(url_path + activate_simple_url,
               load_shortcut_menu
        );
    });
    $(".short-menu-close").click(function(){
        $('#shortcut-menu div').hide();
        $('#shortcut-menu table').hide();
        $(".short-menu-close").hide();
        $(".short-menu-open").show();
        $.get(shortcut_menu_hide_url);
    });
    $(".short-menu-open").click(function(){
        $('#shortcut-menu div').show();
        $('#shortcut-menu table').show();
        $(".short-menu-open").hide();
        $(".short-menu-close").show();
        $.get(shortcut_menu_show_url);
    });
    if (shortcut_menu_hide){
        $('#shortcut-menu div').hide();
        $('#shortcut-menu table').hide();
        $(".short-menu-close").hide();
        $(".short-menu-open").show();
    }
}

function init_shortcut_fields(){
    $("#current_file").change(function(){
        $.post('/' + url_path + 'update-current-item/',
               {item:'file', value:$("#current_file").val()},
               load_shortcut_menu
        );
    });
    $("#current_operation").change(function(){
        $.post('/' + url_path + 'update-current-item/',
               {item:'operation', value:$("#current_operation").val()},
               load_shortcut_menu
        );
    });
    $("#current_contextrecord").change(function(){
        $.post('/' + url_path + 'update-current-item/',
               {item:'contextrecord', value:$("#current_contextrecord").val()},
               load_shortcut_menu
        );
    });
    $("#current_find").change(function(){
        $.post('/' + url_path + 'update-current-item/',
               {item:'find', value:$("#current_find").val()},
               load_shortcut_menu
        );
    });
    $("#current_treatment").change(function(){
        $.post('/' + url_path + 'update-current-item/',
               {item:'treatment', value:$("#current_treatment").val()},
               load_shortcut_menu
        );
    });
    $("#current_treatmentfile").change(function(){
        $.post('/' + url_path + 'update-current-item/',
               {item:'treatmentfile', value:$("#current_treatmentfile").val()},
               load_shortcut_menu
        );
    });
}

function init_advanced_shortcut_fields(){
    $('#id_file-shortcut').change(function(){
        $("#id_select_file-shortcut").attr(
            'title', $('#id_select_file-shortcut').val());
        $.post('/' + url_path + 'update-current-item/',
               {item: "file", value:$("#id_file-shortcut").val()},
               load_shortcut_menu
        );
    });
    $('#id_operation-shortcut').change(function(){
        $("#id_select_operation-shortcut").attr(
            'title', $('#id_select_operation-shortcut').val());
        $.post('/' + url_path + 'update-current-item/',
               {item: "operation", value:$("#id_operation-shortcut").val()},
               load_shortcut_menu
        );
    });
    $('#id_contextrecord-shortcut').change(function(){
        $("#id_select_contextrecord-shortcut").attr(
            'title', $('#id_select_contextrecord-shortcut').val());
        $.post('/' + url_path + 'update-current-item/',
               {item: "contextrecord", value:$("#id_contextrecord-shortcut").val()},
               load_shortcut_menu
        );
    });
    $('#id_find-shortcut').change(function(){
        $("#id_select_find-shortcut").attr(
            'title', $('#id_select_find-shortcut').val());
        $.post('/' + url_path + 'update-current-item/',
               {item: "find", value:$("#id_find-shortcut").val()},
               load_shortcut_menu
        );
    });
}

function display_info(msg){
    $('#message .information .content').html(msg);
    $('#message').fadeIn('slow');
    $('#message .information').fadeIn('slow');
    setTimeout(
        function(){
            $('#message .information').fadeOut('slow');
            $('#message').fadeOut('slow');
        }, 5000);
}

function load_shortcut_menu(){
    if (!shortcut_url) return;
    $("#progress").show();
    $.ajax({
        url: shortcut_url,
        cache: false,
        success:function(html){
            init_shortcut_menu(html);
        },
        error:function(XMLHttpRequest, textStatus, errorThrows){
            $("#progress").hide();
        }
    });
}

$(document).ready(function(){
    $("#main_menu > ul > li > ul").hide();
    $("#main_menu ul ul .selected").parents().show();
    var items = new Array('file', 'operation');
    if ($(document).height() < 1.5*$(window).height()){
        $('#to_bottom_arrow').hide();
        $('#to_top_arrow').hide();
    }
    $('#language_selector').change(function(){
        $('#language_form').submit();
    });
    load_shortcut_menu();
    if ($.isFunction($(".prettyPhoto a").prettyPhoto)){
        $(".prettyPhoto a").prettyPhoto({'social_tools':''});
    }
    $('#current_items select').change(function(){
        $(this).attr('class', $(this).children("option:selected").attr('class'));
    });
    $("a.async-link").click(manage_async_link);
    $(".chosen-select").chosen();
});

$(document).on("click", '#to_bottom_arrow', function(){
  $("html, body").animate({ scrollTop: $(document).height() }, 1000);
});

$(document).on("click", '#to_top_arrow', function(){
  $("html, body").animate({ scrollTop: 0}, 1000);
});

$(document).on("click", '.check-all', function(){
  $(this).closest('table'
        ).find('input:checkbox'
        ).attr('checked', $(this).is(':checked'));
});

$(document).on("click", '#main_menu > ul > li', function(){
    var current_id = $(this).attr('id');
    $("#main_menu ul ul").not($(this).parents('ul')).not($(this).find('ul')
                        ).hide('slow');
    $(this).find('ul').show('slow');
});

/* manage help texts */
$(document).on("click", '.help_display', function(){
    var help_text_id = $(this).attr("href") + "_help";
    $(help_text_id).toggle();
});

$(document).on("click", '#progress-content', function(){
    $('#progress').hide();
});

function long_wait(){
    $('#progress').addClass('long');
    $('#progress').show();
    $('.progress-1').show('slow');
    setTimeout(function(){
        $('.progress-1').hide('slow');
        $('.progress-2').show('slow');
    }, 60000);
    setTimeout(function(){
        $('.progress-2').hide('slow');
        $('.progress-3').show('slow');
    }, 120000);
    setTimeout(function(){
        $('.progress-3').hide('slow');
        $('.progress-4').show('slow');
    }, 180000);
    setTimeout(function(){
        $('.progress-4').hide('slow');
        long_wait();
    }, 240000);
}

var last_window;

function load_window(url, speed, on_success){
    $("#progress").show();
    $.ajax({
        url: url,
        cache: false,
        success:function(html){
            $("#progress").hide();
            $("#window").append(html);
            $("#"+last_window).show();
            $("a[rel^='prettyPhoto']").prettyPhoto({'social_tools':''});
            if (on_success) on_success();
        },
        error:function(XMLHttpRequest, textStatus, errorThrows){
            $("#progress").hide();
        }
    });
}

function load_current_window(url, model_name){
    var id;
    if (advanced_menu){
        id = $("#id_" + model_name + "-shortcut").val();
    } else {
        id = $("#current_" + model_name).val();
    }
    if (!id) return;
    url = url.split('/');
    url[url.length - 1] = id;
    url.push('');
    return load_window(url.join('/'));
}

function load_url(url){
    $("#progress").show();
    $.ajax({
        url: url,
        cache: false,
        success:function(html){
            $("#progress").hide();
        },
        error:function(XMLHttpRequest, textStatus, errorThrows){
            $("#progress").hide();
        }
    });
}

function open_window(url){
    var newwindow = window.open(url, '_blank',
                                'height=400,width=600,scrollbars=yes');
    if (window.focus) {newwindow.focus()}
    return false;
}

function save_and_close_window(name_label, name_pk, item_name, item_pk){
  var main_page = opener.document;
  jQuery(main_page).find("#"+name_label).val(item_name);
  jQuery(main_page).find("#"+name_pk).val(item_pk);
  opener.focus();
  self.close();
}

function save_and_close_window_many(name_label, name_pk, item_name, item_pk){
  var main_page = opener.document;
  var lbl_ = jQuery(main_page).find("#"+name_label);
  var val_ = jQuery(main_page).find("#"+name_pk);
  if (val_.val()){
    var v = lbl_.val();
    v = v.slice(0, v.lastIndexOf(","));
    lbl_.val(v + ", " + item_name + ", ");
    val_.val(val_.val() + ", " + item_pk);
    lbl_.change();
  } else {
    jQuery(main_page).find("#"+name_label).val(item_name);
    jQuery(main_page).find("#"+name_pk).val(item_pk);
  }
  opener.focus();
  self.close();
}

function multiRemoveItem(selItems, name, idx){
    for(id in selItems){
        if(selItems[id] == idx){
            selItems.splice(id, 1);
        }
    }
    jQuery("#selected_"+name+"_"+idx).remove();
}

function closeAllWindows(){
    jQuery("#window > div").hide("slow");
    jQuery("#window").html("");
}

function show_hide_flex(id){
    if ($(id).is(':hidden')){
        $(id).css('display', 'flex');
    } else {
        $(id).hide();
    }
}

var activate_all_search_msg = "Searches in the shortcut menu deals with all items.";
var activate_own_search_msg = "Searches in the shortcut menu deals with only your items.";

function activate_all_search(){
    $('.activate_all_search').removeClass('disabled');
    $('.activate_own_search').addClass('disabled');
    $.get(activate_all_search_url, function(data) {
        display_info(activate_all_search_msg);
    });
    return false;
}

function activate_own_search(){
    $('.activate_own_search').removeClass('disabled');
    $('.activate_all_search').addClass('disabled');
    $.get(activate_own_search_url, function(data) {
        display_info(activate_own_search_msg);
    });
    return false;
}
