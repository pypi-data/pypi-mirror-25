define(['base/js/namespace'], function(Jupyter){
    Jupyter._target = '_self';
});

$('#new_notebook').hide();
$('#open_notebook').hide();
$('#copy_notebook').hide();
$('#rename_notebook').hide();
$('#save_checkpoint').hide();
$('#restore_checkpoint').hide();
$('#kill_and_exit').hide();
$('#trust_notebook').hide();
$('#file_menu .divider').each(function(i, el) { $(el).hide(); });
$('#login_widget').hide();
$('#header-container').hide();
$('#kernel_menu .divider').hide();
$('#menu-change-kernel').hide();

// Disable a link back to the tree view
$('a[title="dashboard"]').attr('href', '#');

window.setTimeout(function() {
  $("#notebook_name").off();
  require(['base/js/events'], function(events) { 
    events.on('set_dirty.Notebook', function(evt, data) { 
      window.parent.postMessage({text: 'mark_dirty', dirty: data.value}, '*');
    }) 
  });
}, 1200);

