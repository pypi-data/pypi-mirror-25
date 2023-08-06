graphsrvPlugins = {
  _plugins : {},
  _instances : {},
  _refcount : 0,

  /**
   * register new plugin
   * @method register
   * @param {String} typ type name for plugin
   * @param {Object} ctor plugin definition
   */

  register : function(typ, plugin) {
    this._plugins[typ] = plugin;
  },

  init : function(config) {
    if(!config.type || !this._plugins[config.type]) {
      console.error("Unknown graphsrv plugin", config);
      return;
    }
    var id = config.type + "-"+(this._refcount++);
    var inst = this._instances[id] = new this._plugins[config.type](id, config);
    var par = scriptTags[scriptTags.length-1].parentNode;
    $(par).append(inst.rootElement());
  },

  finalizeAll : function() {
    var i, par, inst;
    for(i in this._instances) {
      inst = this._instances[i]
      par = $(inst.rootElement()).parent('.column');
      inst.finalize(par.width(), par.height(), par);
    }
  }
}

$(document).ready(function() {
  graphsrvPlugins.finalizeAll();
});
