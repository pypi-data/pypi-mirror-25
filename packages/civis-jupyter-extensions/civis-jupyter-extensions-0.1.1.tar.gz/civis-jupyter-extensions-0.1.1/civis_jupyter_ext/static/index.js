define([
  'base/js/namespace'
], function(
  Jupyter
) {
  function load_ipython_extension() {
    Jupyter.CodeCell.options_default.highlight_modes['magic_text/x-sql'] =
      {'reg':[/^%%civisquery|%civisquery/]} ;
    Jupyter.notebook.events.one('kernel_ready.Kernel', function(){
      Jupyter.notebook.get_cells().map(function(cell){
        if (cell.cell_type === 'code'){ cell.auto_highlight(); } }) ;
    });
  }
  return {
    load_ipython_extension: load_ipython_extension
  };
});
